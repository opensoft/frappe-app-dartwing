# Push Dartwing Frappe App to GitHub

## Step 1: Create GitHub Repo

Go to GitHub and create a new repository:
- **Name**: `frappe-app-dartwing`
- **Organization**: `dartwingers`
- **Description**: Dartwing Frappe backend application
- **Visibility**: Private (or Public)
- **DO NOT** initialize with README, .gitignore, or license (already exists)

## Step 2: Push Existing Code

```bash
cd /home/brett/projects/dartwingers/dartwing/apps/dartwing_frappe

# Verify remote is set
git remote -v
# Should show: origin  git@github.com:dartwingers/frappe-app-dartwing.git

# Push to GitHub
git push -u origin master
```

## Step 3: Verify Setup Scripts

Both bench setups have been updated to clone from GitHub:

✅ `/workBenches/devBenches/frappeBench/.devcontainer/setup-dartwing.sh`
✅ `/dartwingers/dartwing/dartwing-frappe/.devcontainer/setup-dartwing.sh`

Both now use:
```bash
bench get-app git@github.com:dartwingers/frappe-app-dartwing.git
```

## Step 4: Test the Setup

After pushing to GitHub, test in a fresh bench:

```bash
# In frappeBench
cd /home/brett/projects/workBenches/devBenches/frappeBench
# Rebuild devcontainer to test automatic clone

# OR manually test
cd development/frappe-bench
bench get-app git@github.com:dartwingers/frappe-app-dartwing.git
bench --site site1.localhost install-app dartwing_frappe
```

## Step 5: Clean Up

After confirming everything works, delete this temporary folder:

```bash
rm -rf /home/brett/projects/dartwingers/dartwing/apps/
```

The app will now only exist:
1. On GitHub (source of truth)
2. Inside bench `apps/` directories (cloned)

## Final Structure

```
GitHub Repos:
├── dartwingers/dartwing-frappe          # Dartwing bench (devcontainer)
└── dartwingers/frappe-app-dartwing      # Dartwing Frappe app code

Local:
├── /workBenches/devBenches/frappeBench/ # General development bench
│   └── development/frappe-bench/apps/
│       └── dartwing_frappe/             # (cloned from GitHub)
│
└── /dartwingers/dartwing/dartwing-frappe/  # Dartwing project bench
    └── development/frappe-bench/apps/
        └── dartwing_frappe/             # (cloned from GitHub)
```
