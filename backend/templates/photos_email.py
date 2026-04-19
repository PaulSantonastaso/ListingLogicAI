"""
photos_email.py

Builds the photo delivery email content.
Sent when Autoenhance.ai photo editing completes (Item 13).

Stubbed for now — infrastructure ready, wired when Item 13 ships.
"""


def build_photos_delivery_subject(address: str | None) -> str:
    if address:
        return f"Your enhanced photos for {address} are ready"
    return "Your enhanced photos are ready"


def build_photos_delivery_html(
    address: str | None,
    photo_count: int,
    download_url: str,
) -> str:
    address_str = address or "your listing"

    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Your enhanced photos are ready</title>
</head>
<body style="margin:0;padding:0;background:#f5f4f1;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f4f1;padding:40px 20px;">
    <tr>
      <td align="center">
        <table width="100%" cellpadding="0" cellspacing="0" style="max-width:600px;">

          <!-- Brand -->
          <tr>
            <td style="padding-bottom:32px;">
              <span style="font-size:15px;font-weight:700;color:#1a1a1a;">ListingLogicAI</span>
            </td>
          </tr>

          <!-- Main card -->
          <tr>
            <td style="background:#ffffff;border-radius:12px;padding:32px;text-align:center;">
              <p style="margin:0 0 8px 0;font-size:32px;">✨</p>
              <p style="margin:0 0 8px 0;font-size:18px;font-weight:600;color:#1a1a1a;">
                Your enhanced photos are ready
              </p>
              <p style="margin:0 0 24px 0;font-size:13px;color:#8a8a8a;">
                {photo_count} photos from {address_str} have been professionally enhanced —
                color corrected, perspective fixed, and twilight sky replacement
                applied to eligible exteriors.
              </p>
              <a href="{download_url}"
                 style="display:inline-block;background:#1a1a1a;color:#ffffff;text-decoration:none;font-size:13px;font-weight:600;padding:14px 32px;border-radius:8px;">
                ⬇ Download Enhanced Photos
              </a>
              <p style="margin:16px 0 0 0;font-size:11px;color:#b4b2a9;">
                Link valid for 7 days · You can download multiple times
              </p>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="text-align:center;padding-top:32px;">
              <p style="margin:0;font-size:11px;color:#b4b2a9;">
                ListingLogicAI · AI-powered listing marketing
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


def build_photos_delivery_text(
    address: str | None,
    photo_count: int,
    download_url: str,
) -> str:
    address_str = address or "your listing"
    return "\n".join([
        f"Your enhanced photos for {address_str} are ready",
        "=" * 60,
        "",
        f"{photo_count} photos have been professionally enhanced.",
        "Color correction, perspective fix, and twilight sky replacement",
        "applied to eligible exteriors.",
        "",
        "DOWNLOAD YOUR ENHANCED PHOTOS",
        "-" * 40,
        download_url,
        "",
        "Link valid for 7 days. You can download multiple times.",
        "",
        "—",
        "ListingLogicAI · AI-powered listing marketing",
    ])