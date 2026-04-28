"""
photos_email.py

Builds the photo delivery email content.
Sent when Autoenhance.ai photo editing completes.
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
    photo_label = f"{photo_count} photo{'s' if photo_count != 1 else ''}"

    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Your enhanced photos are ready</title>
</head>
<body style="margin:0;padding:0;background:#EFEAE0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#EFEAE0;padding:40px 20px;">
    <tr>
      <td align="center">
        <table width="100%" cellpadding="0" cellspacing="0" style="max-width:600px;">

          <!-- Brand -->
          <tr>
            <td style="padding-bottom:28px;">
              <span style="font-size:16px;font-weight:700;color:#1F3D2E;letter-spacing:-0.3px;">
                metes
              </span>
            </td>
          </tr>

          <!-- Header card -->
          <tr>
            <td style="background:#1F3D2E;border-radius:12px;padding:28px 32px;">
              <p style="margin:0 0 6px 0;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:rgba(244,240,232,0.55);">
                Photo Editing Complete
              </p>
              <p style="margin:0;font-size:20px;font-weight:600;line-height:1.35;color:#F4F0E8;">
                {address_str}
              </p>
            </td>
          </tr>

          <!-- Spacer -->
          <tr><td style="height:12px;"></td></tr>

          <!-- What was applied -->
          <tr>
            <td style="background:#FAF7F0;border-radius:12px;padding:24px 32px;">
              <p style="margin:0 0 14px 0;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#9A7E50;">
                What was applied to {photo_label}
              </p>
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td style="padding:7px 0;border-bottom:1px solid #EFEAE0;">
                    <span style="font-size:13px;color:#1F3D2E;">Color correction &amp; exposure balancing</span>
                  </td>
                </tr>
                <tr>
                  <td style="padding:7px 0;border-bottom:1px solid #EFEAE0;">
                    <span style="font-size:13px;color:#1F3D2E;">Perspective &amp; level correction</span>
                  </td>
                </tr>
                <tr>
                  <td style="padding:7px 0;border-bottom:1px solid #EFEAE0;">
                    <span style="font-size:13px;color:#1F3D2E;">Window pull on interiors</span>
                  </td>
                </tr>
                <tr>
                  <td style="padding:7px 0;">
                    <span style="font-size:13px;color:#1F3D2E;">Sky replacement on eligible exteriors</span>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Spacer -->
          <tr><td style="height:12px;"></td></tr>

          <!-- Download CTA -->
          <tr>
            <td style="background:#FAF7F0;border-radius:12px;padding:28px 32px;text-align:center;">
              <p style="margin:0 0 6px 0;font-size:14px;font-weight:600;color:#14271E;">
                Ready to upload to MLS
              </p>
              <p style="margin:0 0 22px 0;font-size:12px;color:#4A6B53;line-height:1.55;">
                Drop them straight into your MLS upload or share with your client.
              </p>
              <a href="{download_url}"
                 style="display:inline-block;background:#1F3D2E;color:#F4F0E8;text-decoration:none;font-size:13px;font-weight:600;padding:14px 32px;border-radius:8px;">
                Download Enhanced Photos
              </a>
              <p style="margin:16px 0 0 0;font-size:11px;color:#9A7E50;">
                Link valid for 7 days · Download multiple times
              </p>
            </td>
          </tr>

          <!-- Spacer -->
          <tr><td style="height:32px;"></td></tr>

          <!-- Footer -->
          <tr>
            <td style="text-align:center;padding-bottom:20px;">
              <p style="margin:0;font-size:11px;color:#9A7E50;">
                metes · AI-powered listing marketing for high-performing agents
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
        f"{photo_label} professionally enhanced:",
        "  - Color correction & exposure balancing",
        "  - Perspective & level correction",
        "  - Window pull on interiors",
        "  - Sky replacement on eligible exteriors",
        "",
        "Ready to upload straight to MLS.",
        "",
        "DOWNLOAD YOUR ENHANCED PHOTOS",
        "-" * 40,
        download_url,
        "",
        "Link valid for 7 days. Download multiple times.",
        "",
        "—",
        "metes · AI-powered listing marketing",
    ])