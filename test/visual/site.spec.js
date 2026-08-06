const { test, expect } = require("@playwright/test");
const { preparePage, stabilizeVisuals } = require("./helpers");

test.beforeEach(async ({ page }) => {
  await preparePage(page, "light");
});

test("homepage presents the academic profile without private contact details", async ({ page }) => {
  await page.goto("/al-folio/", { waitUntil: "networkidle" });
  await stabilizeVisuals(page);

  await expect(page.getByRole("heading", { level: 1, name: "Shuwei Zhao" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Research Interests" })).toBeVisible();
  await expect(page.getByText("medical robotics, surgical robotics, and magnetic robotics")).toBeVisible();
  await expect(page.getByText(/Prof\. Qiji Ze.s group at Xi.an Jiaotong University/).first()).toBeVisible();
  await expect(page.locator('.contact-icons a[href*="scholar.google.com/citations?user=uUcY21YAAAAJ"]')).toBeVisible();
  await expect(page.locator("a.al-email-protect").first()).toBeVisible();
  await expect(page.locator(".profile")).toHaveCount(0);

  const bodyText = await page.locator("body").innerText();
  expect(bodyText).not.toContain("9572-0915");
  expect(bodyText).not.toContain("+852");
});

test("research page shows the three selected robotics projects", async ({ page }) => {
  await page.goto("/al-folio/research/", { waitUntil: "networkidle" });
  await stabilizeVisuals(page);

  await expect(page.getByRole("heading", { level: 1, name: "research" })).toBeVisible();
  await expect(page.getByRole("heading", { level: 3, name: "Magnetically Steerable Micro-Camera Catheter" })).toBeVisible();
  await expect(page.getByRole("heading", { level: 3, name: "Soft Miniaturized Intraductal Imaging Catheter" })).toBeVisible();
  await expect(page.getByRole("heading", { level: 3, name: "Kirigami Capsule Robot for Gastrointestinal Biopsy" })).toBeVisible();
});

test("publications preserve authorship and current link availability", async ({ page }) => {
  await page.goto("/al-folio/publications/", { waitUntil: "networkidle" });
  await stabilizeVisuals(page);

  const icbir = page.locator("#zhao2026magneticcatheter");
  await expect(icbir).toContainText("Shuwei Zhao and Ruizhou Zhao contributed equally");
  await expect(icbir.locator(".links a")).toHaveCount(0);

  const icra = page.locator("#zhao2026kirigami");
  await expect(icra).toContainText("Shuwei Zhao is the second author");
  await expect(icra).toContainText("Ruizhou Zhao and Yichen Chu are co-first authors");
  await expect(icra.getByRole("button", { name: "PDF" })).toBeVisible();
});

test("CV page exposes the public CV and contact routes", async ({ page }) => {
  await page.goto("/al-folio/cv/", { waitUntil: "networkidle" });
  await stabilizeVisuals(page);

  await expect(page.getByRole("heading", { level: 1, name: "CV" })).toBeVisible();
  await expect(page.locator('a[href$="/assets/pdf/Shuwei_Zhao_CV.pdf"]').first()).toBeVisible();
  await expect(page.getByText("Prof. Bradley Nelson").first()).toBeVisible();
});

test("layout has no horizontal overflow and mobile navigation toggles", async ({ page }, testInfo) => {
  await page.goto("/al-folio/", { waitUntil: "networkidle" });
  await stabilizeVisuals(page);

  const dimensions = await page.evaluate(() => ({
    clientWidth: document.documentElement.clientWidth,
    scrollWidth: document.documentElement.scrollWidth,
  }));
  expect(dimensions.scrollWidth).toBeLessThanOrEqual(dimensions.clientWidth + 1);

  if (testInfo.project.name !== "mobile") {
    return;
  }

  const toggle = page.locator(".navbar-toggler").first();
  const navigation = page.locator(".navbar-collapse").first();
  await expect(toggle).toBeVisible();
  await toggle.click();
  await expect(navigation).toHaveClass(/show/);
  await toggle.click();
  await expect(navigation).not.toHaveClass(/show/);
});
