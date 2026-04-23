"""
photos_email.py

Builds the photo delivery email content.
Sent when Autoenhance.ai photo editing completes (Item 13).
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
              <span style="font-size:15px;font-weight:700;color:#1a1a1a;letter-spacing:-0.3px;">
                ListingLogicAI
              </span>
            </td>
          </tr>

          <!-- Header card -->
          <tr>
            <td style="background:#1a1a1a;border-radius:12px;padding:28px 32px;">
              <p style="margin:0 0 6px 0;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:rgba(255,255,255,0.5);">
                Photo Editing Complete
              </p>
              <p style="margin:0;font-size:18px;font-weight:600;line-height:1.4;color:#ffffff;">
                {address_str}
              </p>
            </td>
          </tr>

          <!-- Spacer -->
          <tr><td style="height:16px;"></td></tr>

          <!-- Detail card -->
          <tr>
            <td style="background:#ffffff;border-radius:12px;padding:28px 32px;">
              <p style="margin:0 0 4px 0;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#8a8a8a;">
                What was applied
              </p>
              <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:16px;">
                <tr>
                  <td style="padding:8px 0;border-bottom:1px solid #f0ede8;">
                    <span style="font-size:13px;color:#1a1a1a;">✓ Color correction</span>
                  </td>
                </tr>
                <tr>
                  <td style="padding:8px 0;border-bottom:1px solid #f0ede8;">
                    <span style="font-size:13px;color:#1a1a1a;">✓ Exposure balancing</span>
                  </td>
                </tr>
                <tr>
                  <td style="padding:8px 0;border-bottom:1px solid #f0ede8;">
                    <span style="font-size:13px;color:#1a1a1a;">✓ Perspective correction</span>
                  </td>
                </tr>
                <tr>
                  <td style="padding:8px 0;border-bottom:1px solid #f0ede8;">
                    <span style="font-size:13px;color:#1a1a1a;">✓ Window pull on interiors</span>
                  </td>
                </tr>
                <tr>
                  <td style="padding:8px 0;">
                    <span style="font-size:13px;color:#1a1a1a;">✓ Sky replacement on eligible exteriors</span>
                  </td>
                </tr>
              </table>
              <p style="margin:16px 0 0 0;font-size:12px;color:#8a8a8a;">
                {photo_count} photo{"s" if photo_count != 1 else ""} enhanced and ready to upload to MLS.
              </p>
            </td>
          </tr>

          <!-- Spacer -->
          <tr><td style="height:16px;"></td></tr>

          <!-- Download CTA -->
          <tr>
            <td style="background:#ffffff;border-radius:12px;padding:28px 32px;text-align:center;">
              <p style="margin:0 0 6px 0;font-size:14px;font-weight:600;color:#1a1a1a;">
                Your enhanced photos are ready to download
              </p>
              <p style="margin:0 0 20px 0;font-size:12px;color:#8a8a8a;">
                Drop them straight into your MLS upload or share with your client.
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

          <!-- Spacer -->
          <tr><td style="height:32px;"></td></tr>

          <!-- Footer -->
          <tr>
            <td style="text-align:center;padding-bottom:20px;">
              <p style="margin:0;font-size:11px;color:#b4b2a9;">
                ListingLogicAI · AI-powered listing marketing for high-performing agents
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
    photo_label = f"{photo_count} photo{'s' if photo_count != 1 else ''}"
    return "\n".join([
        f"Your enhanced photos for {address_str} are ready",
        "=" * 60,
        "",
        f"{photo_label} have been professionally enhanced:",
        "  - Color correction",
        "  - Exposure balancing",
        "  - Perspective correction",
        "  - Window pull on interiors",
        "  - Sky replacement on eligible exteriors",
        "",
        "Drop them straight into your MLS upload or share with your client.",
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