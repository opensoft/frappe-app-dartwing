# Dartwing Frappe App Setup

## Push to GitHub

```bash
cd /home/brett/projects/dartwingers/dartwing/apps/dartwing_frappe

# Add GitHub remote (replace with your actual org/repo)
git remote add origin git@github.com:{YOUR_ORG}/dartwing-frappe.git

# Push to GitHub
git push -u origin master
```

## Update setup-dartwing.sh

After pushing to GitHub, update the setup script at:
`/home/brett/projects/frappe/.devcontainer/setup-dartwing.sh`

Replace the "bench new-app" section (lines 50-65) with:

```bash
# Step 3: Check if app exists
echo -e "${BLUE}[3/4] Checking if app '$APP_NAME' exists...${NC}"
if [ ! -d "apps/$APP_NAME" ]; then
    echo -e "${YELLOW}  → Cloning app '$APP_NAME' from GitHub${NC}"
    bench get-app git@github.com:{YOUR_ORG}/dartwing-frappe.git
    echo -e "${GREEN}  ✓ App cloned successfully${NC}"
else
    echo -e "${GREEN}  ✓ App already exists${NC}"
fi
```

## Alternative: Use HTTPS instead of SSH

If using HTTPS:
```bash
bench get-app https://github.com/{YOUR_ORG}/dartwing-frappe.git
```

This way:
- Team members will automatically clone from GitHub
- App stays in its own separate git repo
- No app code in the environment repo
