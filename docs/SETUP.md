# Setup Guide (no coding needed)

Setup takes about 30–45 minutes. You will need:
1. A **Claude API key** (required). Research and writing don't work without it.
2. A **hosting account** so the form has a public link. Render.com is recommended.
3. Optional: **Google** (Drive and Sheets delivery) and **Slack** (approval notifications).

---

## Step 1: Get a Claude API key (required)
1. Go to https://console.anthropic.com and sign in or create an account.
2. Open **Billing** and add a payment method or credits. The API is billed per use.
3. Open **API Keys**, then **Create Key**. Copy the key (it starts with `sk-ant-`).
4. Keep it private. You'll paste it into the app in Step 3.

**Cost guide.** One full client month (about 20–30 posts, with web research) makes roughly 25–40 Claude requests. Check your usage in the Anthropic Console after the first run. To protect against spam, the app runs at most `MAX_RUNS_PER_DAY` (default 10) briefs per day. Runs beyond that wait as "paused" until you start them.

## Step 2: Put the app online (Render)
1. Create an account at https://render.com and connect your GitHub account.
2. Click **New → Blueprint** and choose the repository `ai-marketing-automation-2`. Render reads `render.yaml` automatically.
3. When asked, fill in:
   - `BASE_URL`: leave it blank for now. After the first deploy, copy your app's address (for example `https://organic-marketing-engine.onrender.com`), set it here, and redeploy.
   - `ANTHROPIC_API_KEY`: paste the key from Step 1, or add it later on the Settings page.
4. Deploy. Render generates the admin password: find it under **Environment → ADMIN_PASSWORD**.
5. Open `https://<your-app>/admin`. Sign in with username `admin` and that password.

The blueprint uses the paid Starter instance because it needs a **persistent disk** to keep the database and client files. On a free instance, your data would be lost on every restart.

## Step 3: Add keys on the Settings page
Open **Settings & integrations** in the dashboard. Paste the Claude API key and click **Save**. The status should change to "configured".

## Step 4 (optional): Connect Google Drive & Sheets
1. Go to https://console.cloud.google.com and create a project (for example "Organic Marketing Engine").
2. **APIs & Services → Library:** enable **Google Drive API** and **Google Sheets API**.
3. **APIs & Services → OAuth consent screen:** choose *External* (or *Internal* if you use Google Workspace), fill in the app name and your email, and add yourself as a test user.
   - Then click **Publish app** ("In production"). If the app stays in *Testing* mode, Google expires the connection every 7 days.
4. **APIs & Services → Credentials → Create credentials → OAuth client ID:**
   - Application type: **Web application**
   - Authorised redirect URI: copy it exactly from the app's Settings page (it looks like `https://<your-app>/admin/google/callback`).
5. Copy the **Client ID** and **Client Secret** into the app's Settings page and click **Save**.
6. Click **Connect Google account** and approve. Google may say the app is unverified. That's expected for your own private app: click *Advanced → Continue*.

After connecting, every completed run creates **My Drive → Organic Social Clients → Organic Social — <Client>**, containing:
- Google Docs for research, strategy, content, creative briefs and QA.
- A **<Client> — Content Calendar** Sheet with one tab per month and an **Approval Status** dropdown.

To use Google on runs that finished before you connected it, open the run and click **Retry skipped delivery/notification steps**.

## Step 5 (optional): Connect Slack
1. Go to https://api.slack.com/apps, then **Create New App → From scratch**, and pick your workspace.
2. **Incoming Webhooks:** turn it on, click **Add New Webhook to Workspace**, and choose the channel for approval requests.
3. Copy the webhook URL (`https://hooks.slack.com/services/...`) into the Settings page and click **Save**.
4. Click **Send test message** to check that it works.

## Step 6: Share the form
Send clients `https://<your-app>/brief`. After a client submits, the run appears on your dashboard. Refresh the page to watch the stages complete. A full run usually takes 15–40 minutes.

## Approving content
- On the run page, set each post to **Approved**, **Changes Requested** or **Rejected**, with an optional comment. If Google is connected, the change is copied to the Sheet.
- Or edit the **Approval Status** column in the Google Sheet, then click **Pull approvals from Google Sheet** on the run page.
- To regenerate part of the work, use **Re-run from** on the run page. Re-running captions, scripts or briefs keeps approved posts unchanged.
- The system never publishes. Post approved content yourself or through your scheduler.

## Troubleshooting
| Problem | Fix |
|---|---|
| Run failed: "Claude is not configured" | Add the API key in Settings, then click **Retry from failed stage** |
| Run failed with a Claude error (rate limit, overloaded) | Wait a few minutes, then click **Retry**. Finished stages are not repeated. |
| Delivery "skipped: Google not connected" | Connect Google (Step 4), then click **Retry skipped delivery/notification steps** |
| Google stops working after a week | Publish the OAuth consent screen (Step 4.3), then reconnect |
| A brief is "paused" | The daily run limit was reached. Open the run and click **Start run**. |
