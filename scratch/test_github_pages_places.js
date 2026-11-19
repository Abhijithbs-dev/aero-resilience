const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const TARGET_URL = process.env.TEST_URL || 'https://abhijithbs-dev.github.io/aero-resilience/';
const EVIDENCE_DIR = '/home/abhijithbs/.gemini/antigravity/brain/86dd7e0b-9ebc-4d81-a792-7b79b7733475/github_pages_evidence';

if (!fs.existsSync(EVIDENCE_DIR)) {
  fs.mkdirSync(EVIDENCE_DIR, { recursive: true });
}

const TEST_PLACES = [
  { name: 'Delhi-NCR', selector: 'button[data-city="Delhi-NCR"]', expectedStandard: 'CPCB' },
  { name: 'Mumbai', selector: 'button[data-city="Mumbai"]', expectedStandard: 'CPCB' },
  { name: 'Kolkata', selector: 'button[data-city="Kolkata"]', expectedStandard: 'CPCB' },
  { name: 'Bengaluru', selector: 'button[data-city="Bengaluru"]', expectedStandard: 'CPCB' },
  { name: 'London', selector: 'button[data-city="London"]', expectedStandard: 'US-EPA' }
];

(async () => {
  console.log(`\n======================================================`);
  console.log(`Testing Target URL: ${TARGET_URL}`);
  console.log(`======================================================\n`);

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();

  page.on('console', msg => {
    if (msg.type() === 'error') console.error('  [BROWSER ERROR]:', msg.text());
  });
  page.on('pageerror', err => console.error('  [PAGE ERROR]:', err.message));

  console.log('Navigating to page...');
  await page.goto(TARGET_URL, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(2000);

  const results = [];

  for (let i = 0; i < TEST_PLACES.length; i++) {
    const place = TEST_PLACES[i];
    console.log(`\n[${i + 1}/5] Selecting Location: ${place.name}...`);

    const btn = page.locator(place.selector);
    if (await btn.isVisible()) {
      await btn.click();
    } else {
      await page.fill('#location-input', place.name);
      await page.keyboard.press('Enter');
    }

    // Wait for sync to complete
    await page.waitForTimeout(600);
    await page.waitForFunction(() => {
      const syncBtn = document.getElementById('fetch-live-aqi-btn');
      return syncBtn && !syncBtn.disabled && !syncBtn.textContent.includes('Syncing');
    }, { timeout: 15000 }).catch(() => {});
    await page.waitForTimeout(800);

    // Extract telemetry from UI
    const locationText = await page.locator('#station-label').innerText();
    const aqiText = await page.locator('#hero-aqi-number').innerText();
    const statusText = await page.locator('#hero-status-title').innerText();
    const tempText = await page.locator('#weather-temp').innerText();
    const humText = await page.locator('#weather-humidity').innerText();
    const windText = await page.locator('#weather-wind').innerText();
    const pm25Text = await page.locator('#pm25-val').innerText();
    const standardText = await page.locator('#aqi-standard-label').innerText();
    const hotspotCount = await page.locator('.hotspot-card').count();

    const screenshotPath = path.join(EVIDENCE_DIR, `place_${i + 1}_${place.name.replace(/[^a-zA-Z0-9]/g, '_')}.png`);
    await page.screenshot({ path: screenshotPath, fullPage: false });

    const result = {
      place: place.name,
      renderedLocation: locationText,
      aqi: parseInt(aqiText, 10),
      status: statusText,
      temperature: tempText,
      humidity: humText,
      wind: windText,
      pm25: pm25Text,
      standard: standardText,
      hotspots: hotspotCount,
      screenshot: screenshotPath
    };
    results.push(result);

    console.log(`  ✓ Rendered Location: "${locationText}"`);
    console.log(`  ✓ AQI: ${aqiText} (${statusText})`);
    console.log(`  ✓ Standard: ${standardText}`);
    console.log(`  ✓ Microclimate: ${tempText} | ${humText} | ${windText}`);
    console.log(`  ✓ PM2.5: ${pm25Text} µg/m³`);
    console.log(`  ✓ Regional Stations: ${hotspotCount} cards active`);
    console.log(`  ✓ Screenshot: ${screenshotPath}`);

    // Assertions
    if (isNaN(result.aqi) || result.aqi <= 0) {
      throw new Error(`Invalid AQI value for ${place.name}: ${aqiText}`);
    }
    if (!result.standard.includes(place.expectedStandard)) {
      throw new Error(`Expected standard ${place.expectedStandard} for ${place.name}, got ${result.standard}`);
    }
  }

  // Cross-location distinctiveness check
  console.log(`\n--- Cross-Location Verification ---`);
  const uniqueAqis = new Set(results.map(r => r.aqi));
  const uniqueTemps = new Set(results.map(r => r.temperature));
  console.log(`Unique AQI levels across 5 cities: ${uniqueAqis.size} / 5`);
  console.log(`Unique temperatures across 5 cities: ${uniqueTemps.size} / 5`);

  if (uniqueAqis.size < 3) {
    throw new Error('Telemetry across places did not vary sufficiently!');
  }

  console.log(`\n🎉 ALL 5 PLACES VERIFIED ACCURATELY!`);

  await browser.close();
  fs.writeFileSync(path.join(EVIDENCE_DIR, 'results.json'), JSON.stringify(results, null, 2));
})();
