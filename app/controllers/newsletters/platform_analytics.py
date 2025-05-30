import io
import logging

import pandas as pd
from fastapi import HTTPException
import asyncio
import httpx

from app.helpers.dist_filter_by_time import _cutoff, TimeWindow, _in_window

"""
Below functions are to make requests to the nl api asynchronously 
but for some reason they don't work for newsletters with many distributions
"""

MAX_RETRIES = 3
RETRY_DELAY = 2


async def fetch_distribution_data(dist, headers, client):
    """
    Fetch analytics for a single distribution asynchronously.
    """
    dist_id = dist["_id"]
    scheduled_date = dist.get("scheduledDate", None) or dist.get("scheduleDate", None)
    status = dist.get("status", None)
    subject = dist.get("newsletterSubject", None) or dist.get("subject", None)
    analytics_url = f"https://nl-api.newsletters.meltwater.io/analytics/get/recipients/{dist_id}"

    try:
        # Fetch total recipients
        response_1 = await client.get(analytics_url, headers=headers, params={"page": "0", "size": "25"})
        response_1.raise_for_status()
        total_recipients = response_1.json()["total"]

        # Fetch detailed data
        response_2 = await client.get(
            analytics_url,
            headers=headers,
            params={"page": "0", "size": total_recipients}
        )
        response_2.raise_for_status()
        recipients = response_2.json()["recipients"]

        # Aggregate metrics and add to out_list

        out_list = [
            {
                "distribution_id": dist_id,
                "subject": subject,
                "scheduled_date": scheduled_date,
                "email_address": r.get("emailAddress", "None"),
                "status": status,
                "opened": r.get("opened", 0),
                "clicked": r.get("clicked", 0),
                "bounced": r.get("bounced", 0),
                "blocked": r.get("blocked", 0),
                "delivered": r.get("delivered", 0),
            }
            for r in recipients
        ]

        logging.info(f"Fetching data for distribution {dist_id}")
        # logging.info(out_list)  # Just for testing
        return out_list

    except httpx.HTTPStatusError as e:
        logging.warning(f"HTTPStatusError occurred for distribution {dist_id}: {str(e)}")
        raise

    except httpx.RequestError as e:
        logging.warning(f"RequestError occurred for distribution {dist_id}: {str(e)}")
        raise

    except Exception as e:
        logging.warning(f"An Exception occurred for distribution {dist_id}: {str(e)}")
        raise


async def fetch_distribution_data_with_retry(dist, headers, client):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return await fetch_distribution_data(dist, headers, client)
        except Exception as e:
            logging.warning(f"Attempt {attempt} failed for {dist['_id']}: {e}")
            if attempt == MAX_RETRIES:
                logging.error(f"Giving up on {dist['_id']} after {MAX_RETRIES} attempts.")
                return [{"distribution_id": dist['_id'],
                         "scheduled_date": dist.get("scheduledDate", None),
                         "error": str(e)}]
            await asyncio.sleep(RETRY_DELAY)


async def get_all_analytics(
        nl_id: str,
        auth_token: str,
        window: TimeWindow = "6m",
        is_new_version: bool = False
):
    """
    Fetch analytics for all distributions asynchronously.
    """
    headers = {
        "accept": "*/*",
        "authorization": auth_token,
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0"
    }

    url = f"https://app.meltwater.com/api/newsletters/newsletter/distribution/{nl_id}/distributions"

    if is_new_version is True:
        url = f"https://nl-bff.newsletters.meltwater.io/newsletter/{nl_id}/distributions"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            
            if is_new_version is True:
                distributions = response.json().get("distributions", [])
            else:
                distributions = response.json()

            if window == "allTime":
                filtered_distributions = distributions
            else:
                boundary = _cutoff(window)
                # Filter distributions by date-range
                filtered_distributions = [d for d in distributions if _in_window(d, boundary)]
                if not filtered_distributions:
                    raise HTTPException(
                        status_code=404,
                        detail=f"No distributions in the last {window}",
                    )

            # Fetch data in parallel using asyncio.gather
            tasks = [fetch_distribution_data_with_retry(dist, headers, client) for dist in filtered_distributions]
            results = await asyncio.gather(*tasks)

            all_rows = [item for sublist in results for item in sublist]

            if not all_rows:
                raise HTTPException(status_code=404, detail="Newsletter not found")

            return all_rows

    except httpx.HTTPStatusError:
        raise HTTPException(status_code=404, detail="Newsletter not found")

    except httpx.RequestError as e:
        logging.warning(f"Error fetching distributions: {e} for newsletter ID: {nl_id}")
        raise HTTPException(status_code=404, detail="Newsletter not found")

    except HTTPException as e:
        logging.warning(f"Error fetching distributions: {e} for newsletter ID: {nl_id}")
        raise e

    except Exception as e:
        logging.warning(f"Error fetching distributions: {e} for newsletter ID: {nl_id}")
        raise HTTPException(status_code=500, detail="Something went wrong")


def convert_to_csv_stream(data):
    """
    Convert a list of dictionaries to a CSV stream.
    """
    df = pd.DataFrame(data)  # Convert to DataFrame
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    stream.seek(0)  # Reset stream position
    return stream  # Return in-memory CSV stream
