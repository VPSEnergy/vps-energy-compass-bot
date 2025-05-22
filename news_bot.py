import os, datetime as dt, textwrap, requests, markdown2

LI_ENDPOINT = "https://api.linkedin.com/v2/ugcPosts"  # puoi usare /rest/ugcPosts con stesso payload

def markdown_to_linkedin(md: str) -> str:
    """Converte Markdown minimale in plain‑text e tronca a 2 900 caratteri."""
    raw_text = markdown2.markdown(md, extras=["strip"])
    return textwrap.shorten(raw_text, width=2900, placeholder="…")


def publish_to_linkedin(md: str, token: str, author: str):
    payload = {
        "author": author,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": markdown_to_linkedin(md)},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }
    resp = requests.post(LI_ENDPOINT, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json().get("id")
