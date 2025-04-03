import logging

from fastapi import HTTPException
import asyncio
import httpx

"""
Below functions are to make requests to the nl api asynchronously 
but for some reason they don't work for newsletters with many distributions
"""


async def fetch_distribution_data(dist, headers, client):
    """
    Fetch analytics for a single distribution asynchronously.
    """
    dist_id = dist["_id"]
    scheduled_date = dist.get("scheduledDate", None)
    status = dist.get("status", None)
    subject = dist.get("newsletterSubject", None)
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
                "email_address": r["emailAddress"],
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
        return {"distribution_id": dist_id,
                "scheduled_date": scheduled_date,
                "success": "true",
                "error": ""}

    except httpx.HTTPStatusError as e:
        logging.warning(f"HTTPStatusError occurred for distribution {dist_id}: {str(e)}")
        return {"distribution_id": dist_id,
                "scheduled_date": scheduled_date,
                "success": "true",
                "error": str(e)}

    except httpx.RequestError as e:
        logging.warning(f"RequestError occurred for distribution {dist_id}: {str(e)}")
        return {"distribution_id": dist_id,
                "scheduled_date": scheduled_date,
                "success": "true",
                "error": str(e)}

    except Exception as e:
        logging.warning(f"An Exception occurred for distribution {dist_id}: {str(e)}")
        return {"distribution_id": dist_id,
                "scheduled_date": scheduled_date,
                "success": "true",
                "error": str(e)}


async def get_all_analytics(nl_id, auth_token):
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

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            distributions = response.json()

            # Fetch data in parallel using asyncio.gather
            tasks = [fetch_distribution_data(dist, headers, client) for dist in distributions]
            final_data = await asyncio.gather(*tasks)

            return final_data

    except httpx.HTTPStatusError:
        raise HTTPException(status_code=404, detail="Newsletter not found")

    except httpx.RequestError as e:
        print(f"Error fetching distributions: {e}")
        return []

    except Exception as e:
        print(f"Error fetching distributions: {e}")
        return []
