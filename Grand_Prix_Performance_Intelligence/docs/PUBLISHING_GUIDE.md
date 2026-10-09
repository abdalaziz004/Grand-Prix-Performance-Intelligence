# Publishing to GitHub and LinkedIn

## Before uploading

1. Extract `Grand_Prix_Performance_Intelligence.zip` to a folder.
2. Check that the `data/raw/` directory contains all 12 CSV files.
3. Run the CSV checks:

   ```bash
   python -m pip install -r requirements.txt
   python scripts/run_analysis.py
   python -m unittest discover -s tests -v
   ```

4. Open `README.md` and make sure the screenshots load from their relative paths.
5. Replace the placeholder GitHub URL in the portfolio files after creating the repository.

## Create the GitHub repository

1. Create a public repository named `Grand-Prix-Performance-Intelligence`.
2. Upload the *contents* of the project folder, not the ZIP file alone.
3. Check that `README.md` is in the root of the repository and displays correctly.
4. Wait for the GitHub Actions workflow to run, then check its status.

## Add it to LinkedIn

- Add the repository link to the Featured section.
- Use `portfolio/LINKEDIN_POST_EN.md` for an English post or `portfolio/LINKEDIN_POST_AR.md` for an Arabic post.
- Add the report preview if you want a visual, but remember that `assets/dashboard_preview.png` is generated from the CSV analysis. The Power BI screenshots are specifically the model and relationship screens.

## File note

The repository doesn't include a `.pbix` binary. It does include the query definitions, DAX measures, model notes, source data, reproducible CSV analysis and selected screenshots from the Power BI work session.
