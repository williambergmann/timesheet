# Azure AD Configuration Guide

This guide walks through setting up Microsoft 365 / Azure AD authentication for the Northstar Timesheet application.

## Prerequisites

- Access to your organization's Azure Portal with permissions to create App Registrations
- The Timesheet application running (locally or in Docker)

---

## Step 1: Create App Registration

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** → **App registrations**
3. Click **New registration**

### Registration Settings

| Field                       | Value                                                                                     |
| --------------------------- | ----------------------------------------------------------------------------------------- |
| **Name**                    | `Northstar Timesheet`                                                                     |
| **Supported account types** | `Accounts in any organizational directory and personal Microsoft accounts` (multi-tenant) |
| **Redirect URI - Platform** | `Web`                                                                                     |
| **Redirect URI - URL**      | See table below                                                                           |

> **Note**: For organization-only access, choose `Accounts in this organizational directory only` instead.

### Redirect URIs by Environment

| Environment        | Redirect URI                            |
| ------------------ | --------------------------------------- |
| Docker (localhost) | `http://localhost/auth/callback`        |
| Local Flask dev    | `http://localhost:5000/auth/callback`   |
| Production         | `https://your-domain.com/auth/callback` |

4. Click **Register**

---

## Step 2: Collect Credentials

After registration, you'll be on the App's **Overview** page. Copy these values:

| Azure Portal Field          | Environment Variable |
| --------------------------- | -------------------- |
| **Application (client) ID** | `AZURE_CLIENT_ID`    |
| **Directory (tenant) ID**   | `AZURE_TENANT_ID`    |

---

## Step 3: Create Client Secret

1. Go to **Certificates & secrets** (left sidebar)
2. Click **New client secret**
3. Configure:
   - **Description**: `Timesheet App Secret`
   - **Expires**: Choose based on your security policy (recommended: 12-24 months)
4. Click **Add**
5. **IMPORTANT**: Copy the **Value** immediately (it won't be shown again)

| Azure Portal Field | Environment Variable  |
| ------------------ | --------------------- |
| **Secret Value**   | `AZURE_CLIENT_SECRET` |

---

## Step 4: Configure API Permissions

1. Go to **API permissions** (left sidebar)
2. Verify `User.Read` is present (added by default)
3. If not, click **Add a permission** → **Microsoft Graph** → **Delegated permissions**
4. Search for and add: `User.Read`
5. Click **Grant admin consent for [Your Organization]** (if you have admin rights)

### Required Permissions

| API             | Permission  | Type      | Description                   |
| --------------- | ----------- | --------- | ----------------------------- |
| Microsoft Graph | `User.Read` | Delegated | Sign in and read user profile |

---

## Step 5: Update Environment Variables

### Option A: Docker (.env file in docker/ directory)

Create or edit `docker/.env`:

```bash
# Microsoft 365 / Azure AD
AZURE_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
AZURE_CLIENT_SECRET=your-secret-value-here
AZURE_TENANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
AZURE_REDIRECT_URI=http://localhost/auth/callback
```

### Option B: Local Development (.env in project root)

```bash
# Microsoft 365 / Azure AD
AZURE_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
AZURE_CLIENT_SECRET=your-secret-value-here
AZURE_TENANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
AZURE_REDIRECT_URI=http://localhost:5000/auth/callback
```

---

## Step 6: Restart the Application

### Docker

```bash
cd docker
docker-compose down
docker-compose up --build
```

### Local Development

```bash
# Stop the running Flask app (Ctrl+C)
flask run
```

---

## Step 7: Test Authentication

1. Open `http://localhost` (Docker) or `http://localhost:5000` (local)
2. You should be redirected to Microsoft login
3. Sign in with your Microsoft 365 account
4. Grant consent for the app to read your profile
5. You should be redirected back to the Timesheet dashboard

---

## Troubleshooting

### "AADSTS50011: The redirect URI does not match"

The redirect URI in Azure doesn't match what the app is sending.

**Fix**:

1. Go to App Registration → **Authentication**
2. Add the exact redirect URI your app is using
3. Common URIs to add:
   - `http://localhost/auth/callback`
   - `http://localhost:5000/auth/callback`

### "AADSTS7000218: Request body must contain client_secret"

The client secret is missing or incorrect.

**Fix**:

1. Verify `AZURE_CLIENT_SECRET` is set in your `.env` file
2. Make sure you copied the **Value**, not the **Secret ID**
3. If the secret expired, create a new one

### "AADSTS65001: User or admin has not consented"

The user needs to consent to the app permissions.

**Fix**:

1. Go to App Registration → **API permissions**
2. Click **Grant admin consent for [Organization]**
3. Or: Individual users will be prompted to consent on first login

### Still seeing "DEV MODE: Bypassing Azure AD authentication"

The app is not detecting valid Azure credentials.

**Fix**:

1. Verify all three env vars are set: `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID`
2. Make sure values don't contain "your-azure" placeholder text
3. Restart the application after changing `.env`

### Microsoft Login Button Fails (No Redirect)

Clicking "Sign in with Microsoft" on the landing page results in an error or no response.

**Common Causes & Fixes**:

1. **Azure credentials not configured**

   - Without valid `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, and `AZURE_TENANT_ID`, the Microsoft login cannot work
   - The app will show dev login buttons when credentials are missing - use those instead
   - To enable Microsoft Login: follow Steps 1-5 above to configure Azure AD

2. **MSAL scope configuration error**

   - **Symptom**: `ValueError` or 500 error mentioning scopes
   - **Cause**: Reserved OIDC scopes (`openid`, `profile`, `email`) are explicitly listed
   - **Fix**: Remove reserved scopes from `AZURE_SCOPES` in `app/config.py` - MSAL adds them automatically

3. **Redirect URI mismatch (AADSTS50011)**

   - The Azure app registration redirect URI must match **exactly**:
     - Docker: `http://localhost/auth/callback`
     - Local Flask: `http://localhost:5000/auth/callback`
   - Check for trailing slashes, http vs https, and port numbers

4. **Expired or invalid client secret**

   - Client secrets expire (check Azure Portal → Certificates & secrets)
   - Create a new secret and update `AZURE_CLIENT_SECRET`

5. **Network/firewall blocking Azure endpoints**
   - Ensure the app can reach `login.microsoftonline.com` and `graph.microsoft.com`

### Microsoft Login Works, But User Gets 500 Error After Callback

Authentication succeeds but the callback fails.

**Common Causes & Fixes**:

1. **State/nonce validation failure**

   - Clear browser cookies and try again
   - Check that `SECRET_KEY` hasn't changed between requests

2. **Database user creation fails**

   - Check database connectivity and migrations are up to date
   - Run `flask db upgrade` to ensure user table schema is current

3. **Session cookie issues**
   - In production (HTTPS), ensure `SESSION_COOKIE_SECURE=True`
   - For localhost development over HTTP, set `SESSION_COOKIE_SECURE=False`

### "Internal Server Error" with Duplicate Key Violation

**Symptom**: Clicking login results in:

```
IntegrityError: duplicate key value violates unique constraint "users_azure_id_key"
DETAIL: Key (azure_id)=(dev-user-001) already exists.
```

**Cause**: The dev authentication flow tries to INSERT a new user instead of finding the existing one.

**Fixes**:

1. **Immediate workaround - Reset the database**:

   ```bash
   cd docker
   docker compose down -v   # Removes volumes (database data)
   docker compose up --build -d
   ```

2. **Code fix required** (see BUG-002 in BUGS.md):

   - The auth route should use `get_or_create` pattern
   - Query for existing user by `azure_id` before inserting
   - Example fix in `app/routes/auth.py`:
     ```python
     # Instead of always creating new user:
     user = User.query.filter_by(azure_id=azure_id).first()
     if not user:
         user = User(azure_id=azure_id, ...)
         db.session.add(user)
     db.session.commit()
     ```

3. **Manual database fix** (without losing data):
   ```bash
   docker exec -it timesheet-db-1 psql -U postgres -d timesheet
   # Then in psql:
   DELETE FROM users WHERE azure_id = 'dev-user-001';
   \q
   ```

---

## Security Notes

- **Never commit `.env` files** to version control (they're in `.gitignore`)
- **Rotate client secrets** periodically (before expiration)
- **Use HTTPS in production** - update redirect URI accordingly
- **Principle of least privilege** - only request `User.Read` scope

---

## 🔄 Production Credential Rotation (P0)

Before deploying to production, you **must** create new credentials. Development placeholders are not secure.

### Rotate Azure Client Secret

Azure client secrets expire. Create a new secret before production deployment and set calendar reminders for rotation.

**Step 1: Create a new secret**

1. Go to [Azure Portal](https://portal.azure.com) → **App registrations** → **Northstar Timesheet**
2. Navigate to **Certificates & secrets** → **Client secrets**
3. Click **New client secret**
4. Set description: `Production - Expires YYYY-MM-DD`
5. Choose expiration: **24 months** (recommended) or per security policy
6. Click **Add** and **immediately copy the Value**

**Step 2: Update production environment**

```bash
# Update .env file
AZURE_CLIENT_SECRET=your-new-secret-value-here
```

**Step 3: Set expiration reminder**

Add a calendar reminder 30 days before expiration to rotate again.

**Step 4: Restart the application**

```bash
docker compose -f docker/docker-compose.prod.yml down
docker compose -f docker/docker-compose.prod.yml up -d
```

### Monitor Secret Expiration

Check secret expiration dates via Azure CLI:

```bash
# List all secrets for your app
az ad app credential list --id $AZURE_CLIENT_ID --query "[].{description:displayName, expires:endDateTime}" -o table
```

**Example output:**

```
Description              Expires
-----------------------  -------------------------
Production - 2027-01-12  2027-01-12T00:00:00+00:00
```

### Rotation Checklist

| Task                                                     | Status |
| -------------------------------------------------------- | ------ |
| Create new client secret in Azure Portal                 | ⬜     |
| Copy secret value immediately (shown only once)          | ⬜     |
| Update `AZURE_CLIENT_SECRET` in production `.env`        | ⬜     |
| Restart application                                      | ⬜     |
| Verify login works with new secret                       | ⬜     |
| Set calendar reminder for next rotation                  | ⬜     |
| Delete old secret from Azure Portal (after verification) | ⬜     |

---

## Optional: Add More Redirect URIs

If you need multiple environments, you can add additional redirect URIs:

1. Go to App Registration → **Authentication**
2. Under **Web** → **Redirect URIs**, click **Add URI**
3. Add all environments you need:
   - `http://localhost/auth/callback`
   - `http://localhost:5000/auth/callback`
   - `https://staging.example.com/auth/callback`
   - `https://timesheet.example.com/auth/callback`

---

## Reference: Environment Variables

| Variable              | Description                                   | Example                                |
| --------------------- | --------------------------------------------- | -------------------------------------- |
| `AZURE_CLIENT_ID`     | Application (client) ID from App Registration | `12345678-1234-1234-1234-123456789abc` |
| `AZURE_CLIENT_SECRET` | Client secret value                           | `abc123~xxxxxxxxxxxxxxxxxxxxxx`        |
| `AZURE_TENANT_ID`     | Directory (tenant) ID                         | `87654321-4321-4321-4321-cba987654321` |
| `AZURE_REDIRECT_URI`  | OAuth callback URL                            | `http://localhost/auth/callback`       |

---

## 🚀 Hosting on Azure

### Hosting Options Comparison

| Option                        | Cost/Month                   | Best For                                 | Complexity      |
| ----------------------------- | ---------------------------- | ---------------------------------------- | --------------- |
| **Azure App Service**         | $13-55 (Free tier available) | Quick deployment, managed infrastructure | ⭐ Easy         |
| **Azure Container Apps**      | Pay-per-use                  | Docker containers, autoscaling           | ⭐⭐ Medium     |
| **Azure Container Instances** | ~$30-50                      | Simple container deployment              | ⭐⭐ Medium     |
| **Azure VM**                  | ~$15-40                      | Full control, existing Docker setup      | ⭐⭐⭐ Advanced |

---

### Option 1: Azure App Service (Recommended)

Azure App Service is the easiest way to host this application with managed infrastructure.

#### Prerequisites

```bash
# Install Azure CLI
brew install azure-cli  # macOS
# or: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash  # Linux

# Login to Azure
az login
```

#### Step 1: Create Resource Group

```bash
az group create --name northstar-rg --location eastus
```

#### Step 2: Create Azure Database for PostgreSQL

```bash
# Create PostgreSQL Flexible Server
az postgres flexible-server create \
  --resource-group northstar-rg \
  --name northstar-db \
  --location eastus \
  --admin-user timesheet \
  --admin-password "YourSecurePassword123!" \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --storage-size 32 \
  --version 15

# Create the database
az postgres flexible-server db create \
  --resource-group northstar-rg \
  --server-name northstar-db \
  --database-name timesheet

# Allow Azure services to connect
az postgres flexible-server firewall-rule create \
  --resource-group northstar-rg \
  --name northstar-db \
  --rule-name AllowAzure \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

#### Step 3: Create App Service Plan and Web App

```bash
# Create App Service Plan
az appservice plan create \
  --resource-group northstar-rg \
  --name northstar-plan \
  --sku B1 \
  --is-linux

# Create Web App with Python
az webapp create \
  --resource-group northstar-rg \
  --plan northstar-plan \
  --name northstar-timesheet \
  --runtime "PYTHON:3.11"
```

#### Step 4: Configure Environment Variables

```bash
az webapp config appsettings set \
  --resource-group northstar-rg \
  --name northstar-timesheet \
  --settings \
    AZURE_CLIENT_ID="your-client-id" \
    AZURE_CLIENT_SECRET="your-client-secret" \
    AZURE_TENANT_ID="your-tenant-id" \
    AZURE_REDIRECT_URI="https://northstar-timesheet.azurewebsites.net/auth/callback" \
    DATABASE_URL="postgresql://timesheet:YourSecurePassword123!@northstar-db.postgres.database.azure.com:5432/timesheet?sslmode=require" \
    SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')" \
    FLASK_ENV="production"
```

#### Step 5: Update Azure App Registration

Add the production redirect URI to your App Registration:

1. Go to [Azure Portal](https://portal.azure.com) → **App registrations** → **Northstar Timesheet**
2. Navigate to **Authentication**
3. Add redirect URI: `https://northstar-timesheet.azurewebsites.net/auth/callback`
4. Save changes

#### Step 6: Deploy the Application

**Option A: Deploy from Local Git**

```bash
# Configure deployment source
az webapp deployment source config-local-git \
  --resource-group northstar-rg \
  --name northstar-timesheet

# Get the deployment URL
az webapp deployment source config-local-git \
  --resource-group northstar-rg \
  --name northstar-timesheet \
  --query url --output tsv

# Add Azure remote and push
git remote add azure <deployment-url>
git push azure main
```

**Option B: Deploy from GitHub Actions**

```bash
# Get publish profile
az webapp deployment list-publishing-profiles \
  --resource-group northstar-rg \
  --name northstar-timesheet \
  --xml > publish-profile.xml
```

Then add the contents to GitHub Secrets as `AZURE_WEBAPP_PUBLISH_PROFILE`.

#### Step 7: Run Database Migrations

```bash
# SSH into the web app
az webapp ssh --resource-group northstar-rg --name northstar-timesheet

# Inside the SSH session
cd /home/site/wwwroot
flask db upgrade
```

#### Step 8: Verify Deployment

Open `https://northstar-timesheet.azurewebsites.net` in your browser.

---

### Option 2: Azure Container Apps

For Docker-based deployment with automatic scaling.

#### Step 1: Create Container Registry

```bash
az acr create \
  --resource-group northstar-rg \
  --name northstarcr \
  --sku Basic

az acr login --name northstarcr
```

#### Step 2: Build and Push Docker Image

```bash
# Build the image
docker build -t northstarcr.azurecr.io/timesheet:latest -f docker/Dockerfile .

# Push to Azure Container Registry
docker push northstarcr.azurecr.io/timesheet:latest
```

#### Step 3: Create Container App

```bash
az containerapp create \
  --name northstar-timesheet \
  --resource-group northstar-rg \
  --image northstarcr.azurecr.io/timesheet:latest \
  --target-port 5000 \
  --ingress external \
  --registry-server northstarcr.azurecr.io \
  --env-vars \
    AZURE_CLIENT_ID="your-client-id" \
    AZURE_CLIENT_SECRET="your-client-secret" \
    DATABASE_URL="postgresql://..."
```

---

### Option 3: Azure Container Instances (ACI)

For simple container deployment without orchestration.

```bash
az container create \
  --resource-group northstar-rg \
  --name northstar-timesheet \
  --image northstarcr.azurecr.io/timesheet:latest \
  --dns-name-label northstar-timesheet \
  --ports 5000 \
  --environment-variables \
    AZURE_CLIENT_ID="your-client-id" \
    AZURE_CLIENT_SECRET="your-client-secret" \
    DATABASE_URL="postgresql://..."
```

---

### Option 4: Azure Virtual Machine

For full control with existing Docker Compose setup.

```bash
# Create VM
az vm create \
  --resource-group northstar-rg \
  --name northstar-vm \
  --image Ubuntu2204 \
  --size Standard_B2s \
  --admin-username azureuser \
  --generate-ssh-keys

# Open ports
az vm open-port --port 80 --resource-group northstar-rg --name northstar-vm
az vm open-port --port 443 --resource-group northstar-rg --name northstar-vm

# SSH into VM and set up Docker
ssh azureuser@<vm-public-ip>
# Then install Docker and run docker compose up
```

---

### Production Checklist

Before going live, ensure:

- [ ] SSL/HTTPS enabled (App Service provides free certificates)
- [ ] `AZURE_REDIRECT_URI` uses `https://` URL
- [ ] `SESSION_COOKIE_SECURE=True` in production config
- [ ] Strong `SECRET_KEY` generated (not placeholder)
- [ ] Database backups configured
- [ ] Application Insights enabled for monitoring
- [ ] Rate limiting enabled (REQ-042)
- [ ] Health check endpoint configured (REQ-043)

---

### Estimated Monthly Costs

| Service     | Tier           | Cost           |
| ----------- | -------------- | -------------- |
| App Service | B1 (Basic)     | ~$13/month     |
| PostgreSQL  | Burstable B1ms | ~$15/month     |
| **Total**   |                | **~$28/month** |

Free tier available for testing:

- App Service F1 (free, limited hours)
- PostgreSQL Burstable B1ms (750 hours free first year on new accounts)

---

_Document updated January 12, 2026_
