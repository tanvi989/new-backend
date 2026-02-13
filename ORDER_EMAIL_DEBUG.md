# Order confirmation email – debug guide

## 1. Check if email service is loaded

With the backend running (e.g. `python app.py` on port 5000), open:

**http://localhost:5000/api/health**

In the JSON response check:

- **`order_email_ready`**: `true` = order emails will be sent, `false` = they will not (see below).
- **`order_email_note`**: present only when `order_email_ready` is false; explains that order emails are disabled.

If `order_email_ready` is **false**:

- Backend could not load the notification (MSG91) service.
- In the **backend console** (where you ran `python app.py`) look for one of:
  - `[ORDER EMAIL] Notification service READY` → service loaded (if health still says false, restart backend and check health again).
  - `[ORDER EMAIL] Notification service NOT loaded` or `FAILED to init` → fix MSG91 config (see step 2).

## 2. MSG91 config (in `newbackend/.env`)

Ensure these are set and correct:

- `MSG91_AUTH_KEY` – your MSG91 auth key
- `MSG91_DOMAIN` – e.g. `email.multifolks.com`
- `MSG91_ORDER_TEMPLATE_ID=order_placed_23`
- `MSG91_SENDER_EMAIL` – e.g. `support@multifolks.com`

Restart the backend after changing `.env`.

## 2b. Payment success URL (for Stripe redirect to your success page)

If you use **http://localhost:3001/payment/success** after payment, set in `newbackend/.env`:

```env
PAYMENT_SUCCESS_URL=http://localhost:3001/payment/success
```

Then Stripe will redirect to that URL with `?order_id=...&session_id=...` and the frontend will request the confirmation email from there.

## 3. Confirm which backend the frontend uses

- Frontend on **http://localhost:3001** should use **http://localhost:5000** for the API (see `frontend/.env`: `VITE_API_TARGET` / `VITE_API_URL`).
- If the frontend points to a **live** backend, the order is created and the email is sent from the **live** server (and the recipient is the logged-in user’s email on that server).

## 4. When you place an order – backend console

When you place an order, watch the **backend terminal**. You should see one of:

- `[ORDER EMAIL] Attempting to send to 'your@email.com' for order ... (POST /orders).` or `(create-session).`
- Then either:
  - `[ORDER EMAIL] SENT to your@email.com for order ...` → email was sent.
  - `[ORDER EMAIL] NOT SENT to ...` → check the reason in the same line (e.g. MSG91 error, no email, service not loaded).

If you see **no** `[ORDER EMAIL]` lines:

- The request may not be hitting this backend (e.g. frontend using another API URL).
- Or the order-creation path that sends the email was not run (e.g. different payment/flow).

## 5. Recipient address

The email is sent to the **logged-in user’s email** (the one stored in the account used to place the order). Check that address (and its Spam/Promotions folder).

## 6. Quick test (no order)

From the backend folder:

```bash
python test_order_template.py
```

This sends one test order email to the address in `test_order_template.py` (e.g. paradkartanvii@gmail.com). If this works but real orders don’t, the problem is in the order flow or which backend the app is using.
