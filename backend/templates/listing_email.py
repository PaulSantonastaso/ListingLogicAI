"""
listing_email.py

Builds the listing delivery email content.
Called immediately after Stripe payment confirmation.
"""


def build_listing_delivery_subject(address: str | None) -> str:
    if address:
        return f"Your listing package for {address} is ready"
    return "Your listing package is ready"


def build_listing_delivery_html(
    address: str | None,
    headline: str | None,
    download_url: str,
    preview_url: str,
) -> str:
    address_str = address or "your listing"

    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Your listing package is ready</title>
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
                Listing Package Ready
              </p>
              <p style="margin:0;font-size:20px;font-weight:600;line-height:1.35;color:#F4F0E8;">
                {address_str}
              </p>
            </td>
          </tr>

          <!-- Spacer -->
          <tr><td style="height:12px;"></td></tr>

          <!-- What's included -->
          <tr>
            <td style="background:#FAF7F0;border-radius:12px;padding:24px 32px;">
              <p style="margin:0 0 14px 0;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#9A7E50;">
                What&apos;s in your package
              </p>
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td style="padding:7px 0;border-bottom:1px solid #EFEAE0;">
                    <span style="font-size:13px;color:#1F3D2E;">MLS-ready listing description</span>
                  </td>
                </tr>
                <tr>
                  <td style="padding:7px 0;border-bottom:1px solid #EFEAE0;">
                    <span style="font-size:13px;color:#1F3D2E;">Social launch pack — Facebook + Instagram</span>
                  </td>
                </tr>
                <tr>
                  <td style="padding:7px 0;border-bottom:1px solid #EFEAE0;">
                    <span style="font-size:13px;color:#1F3D2E;">4-email campaign sequence</span>
                  </td>
                </tr>
                <tr>
                  <td style="padding:7px 0;">
                    <span style="font-size:13px;color:#1F3D2E;">Fair Housing compliance audit</span>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Spacer -->
          <tr><td style="height:12px;"></td></tr>

          <!-- CTA card -->
          <tr>
            <td style="background:#FAF7F0;border-radius:12px;padding:28px 32px;text-align:center;">
              <p style="margin:0 0 6px 0;font-size:14px;font-weight:600;color:#14271E;">
                Ready to use
              </p>
              <p style="margin:0 0 22px 0;font-size:12px;color:#4A6B53;line-height:1.55;">
                View your full campaign online or download everything as a ZIP — your call.
              </p>
              <a href="{preview_url}"
                 style="display:inline-block;background:#1F3D2E;color:#F4F0E8;text-decoration:none;font-size:13px;font-weight:600;padding:14px 32px;border-radius:8px;">
                View Listing Package →
              </a>
              <p style="margin:18px 0 10px 0;font-size:11px;color:#9A7E50;">or</p>
              <a href="{download_url}"
                 style="display:inline-block;color:#1F3D2E;text-decoration:none;font-size:12px;font-weight:600;padding:10px 24px;border-radius:8px;border:1px solid #B89968;">
                Download ZIP
              </a>
              <p style="margin:16px 0 0 0;font-size:11px;color:#9A7E50;">
                Link valid for 7 days · Return anytime
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


def build_listing_delivery_text(
    address: str | None,
    headline: str | None,
    download_url: str,
    preview_url: str,
) -> str:
    address_str = address or "your listing"
    return "\n".join([
        f"Your listing package for {address_str} is ready",
        "=" * 60,
        "",
        "What's included:",
        "  - MLS-ready listing description",
        "  - Social launch pack — Facebook + Instagram",
        "  - 4-email campaign sequence",
        "  - Fair Housing compliance audit",
        "",
        "VIEW YOUR LISTING PACKAGE",
        "-" * 40,
        preview_url,
        "",
        "Or download directly:",
        download_url,
        "",
        "Link valid for 7 days. Return anytime.",
        "",
        "—",
        "metes · AI-powered listing marketing",
    ])