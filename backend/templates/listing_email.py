"""
listing_email.py

Builds the listing delivery email content.
Called immediately after Stripe payment confirmation.

Email contains:
  - Listing headline (prominent)
  - MLS description (full text, inline)
  - Just Listed email subject + preview text
  - Download link (7-day TTL, multi-use)

No attachments — content inline, download link for ZIP.
Avoids email size limits and corporate spam filters.
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
    headline_str = headline or ""

    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Your listing package is ready</title>
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

          <!-- Headline card -->
          <tr>
            <td style="background:#1a1a1a;border-radius:12px;padding:28px 32px;">
              <p style="margin:0 0 6px 0;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:rgba(255,255,255,0.5);">
                Listing Headline
              </p>
              <p style="margin:0;font-size:18px;font-weight:600;line-height:1.4;color:#ffffff;">
                {headline_str}
              </p>
            </td>
          </tr>

          <!-- Spacer -->
          <tr><td style="height:16px;"></td></tr>

          <!-- CTA card -->
          <tr>
            <td style="background:#ffffff;border-radius:12px;padding:28px 32px;text-align:center;">
              <p style="margin:0 0 6px 0;font-size:14px;font-weight:600;color:#1a1a1a;">
                Your listing package for {address_str} is ready
              </p>
              <p style="margin:0 0 20px 0;font-size:12px;color:#8a8a8a;">
                MLS description, social posts, email campaign, and compliance audit — all ready to use.
              </p>
              <a href="{preview_url}"
                 style="display:inline-block;background:#1a1a1a;color:#ffffff;text-decoration:none;font-size:13px;font-weight:600;padding:14px 32px;border-radius:8px;">
                View Your Listing Package →
              </a>
              <p style="margin:20px 0 12px 0;font-size:11px;color:#b4b2a9;">or</p>
              <a href="{download_url}"
                 style="display:inline-block;color:#1a1a1a;text-decoration:none;font-size:12px;font-weight:600;padding:10px 24px;border-radius:8px;border:1px solid #e0ddd8;">
                ⬇ Download Package
              </a>
              <p style="margin:16px 0 0 0;font-size:11px;color:#b4b2a9;">
                Link valid for 7 days · You can return anytime
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


def build_listing_delivery_text(
    address: str | None,
    headline: str | None,
    download_url: str,
    preview_url: str,
) -> str:
    address_str = address or "your listing"
    lines = [
        f"Your listing package for {address_str} is ready",
        "=" * 60,
        "",
    ]
    if headline:
        lines += [headline, ""]
    lines += [
        "VIEW YOUR LISTING PACKAGE",
        "-" * 40,
        preview_url,
        "",
        "Or download directly:",
        download_url,
        "",
        "Link valid for 7 days. You can return anytime.",
        "",
        "—",
        "ListingLogicAI · AI-powered listing marketing",
    ]
    return "\n".join(lines)