import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

/* ---------------------------------------------------------------------------
   The catalogue and the shipping table live HERE, on the server.
   The browser only ever sends { slug, qty } pairs and a country code, so a
   tampered request cannot change a price, a shipping fee or a product name.
   Generated from build/content.py — edit prices there and re-run the build.
--------------------------------------------------------------------------- */
const CATALOG = {
  "field5": {
    "name": "FIELD5",
    "tagline": "48V phantom-powered contact microphone",
    "serial": "AL-F5",
    "price": 15500,
    "image": "media/field5-1.sm.jpg"
  },
  "crt2": {
    "name": "CRT2",
    "tagline": "Submersible contact microphone",
    "serial": "AL-C2",
    "price": 6000,
    "image": "media/crt2-1.sm.jpg"
  },
  "crt1": {
    "name": "CRT1",
    "tagline": "Entry contact microphone",
    "serial": "AL-C1",
    "price": 4500,
    "image": "media/crt1-1.sm.jpg"
  },
  "ert": {
    "name": "ERT",
    "tagline": "Electromagnetic (EMF) microphone",
    "serial": "AL-E1",
    "price": 4000,
    "image": "media/ert-1.sm.jpg"
  },
  "raincatcher": {
    "name": "RAINCATCHER",
    "tagline": "Rain plate for FIELD5",
    "serial": "AL-RC",
    "price": 4500,
    "image": "media/raincatcher-1.sm.jpg"
  }
};

const SHIPPING = {
  "RO": {
    "name": "Romania",
    "amount": 500
  },
  "BG": {
    "name": "Bulgaria",
    "amount": 1000
  },
  "CZ": {
    "name": "Czech Republic",
    "amount": 1000
  },
  "HR": {
    "name": "Croatia",
    "amount": 1000
  },
  "CY": {
    "name": "Cyprus",
    "amount": 1000
  },
  "GR": {
    "name": "Greece",
    "amount": 1000
  },
  "SK": {
    "name": "Slovakia",
    "amount": 1000
  },
  "SI": {
    "name": "Slovenia",
    "amount": 1000
  },
  "DE": {
    "name": "Germany",
    "amount": 1200
  },
  "HU": {
    "name": "Hungary",
    "amount": 1200
  },
  "PL": {
    "name": "Poland",
    "amount": 1200
  },
  "AT": {
    "name": "Austria",
    "amount": 1300
  },
  "FR": {
    "name": "France",
    "amount": 1400
  },
  "IT": {
    "name": "Italy",
    "amount": 1400
  },
  "PT": {
    "name": "Portugal",
    "amount": 1400
  },
  "ES": {
    "name": "Spain",
    "amount": 1500
  },
  "EE": {
    "name": "Estonia",
    "amount": 1500
  },
  "LV": {
    "name": "Latvia",
    "amount": 1500
  },
  "LT": {
    "name": "Lithuania",
    "amount": 1500
  },
  "NL": {
    "name": "Netherlands",
    "amount": 1700
  },
  "IE": {
    "name": "Ireland",
    "amount": 1800
  },
  "LU": {
    "name": "Luxembourg",
    "amount": 2000
  },
  "DK": {
    "name": "Denmark",
    "amount": 2000
  },
  "BE": {
    "name": "Belgium",
    "amount": 2200
  },
  "SE": {
    "name": "Sweden",
    "amount": 2500
  },
  "CH": {
    "name": "Switzerland",
    "amount": 2500
  },
  "US": {
    "name": "USA",
    "amount": 3000
  },
  "GB": {
    "name": "United Kingdom",
    "amount": 2600
  },
  "FI": {
    "name": "Finland",
    "amount": 4000
  }
};

const MAX_QTY = 20;

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { items, country } = req.body || {};

  if (!Array.isArray(items) || items.length === 0) {
    return res.status(400).json({ error: 'Cart is empty' });
  }
  if (items.length > 20) {
    return res.status(400).json({ error: 'Too many line items' });
  }
  if (typeof country !== 'string' || !Object.prototype.hasOwnProperty.call(SHIPPING, country)) {
    return res.status(400).json({ error: 'We do not ship to that country yet' });
  }

  // Merge duplicate slugs, validate quantities, and price everything from CATALOG.
  const qtyBySlug = new Map();
  for (const item of items) {
    const slug = item && typeof item.slug === 'string' ? item.slug : null;
    const product = slug && Object.prototype.hasOwnProperty.call(CATALOG, slug) ? CATALOG[slug] : null;
    if (!product) {
      return res.status(400).json({ error: 'Unknown product' });
    }
    const qty = typeof item.qty === 'number' ? item.qty : Number(item.qty);
    if (!Number.isInteger(qty) || qty < 1) {
      return res.status(400).json({ error: 'Invalid quantity' });
    }
    const total = (qtyBySlug.get(slug) || 0) + qty;
    if (total > MAX_QTY) {
      return res.status(400).json({ error: `Maximum ${MAX_QTY} units of ${product.name} per order` });
    }
    qtyBySlug.set(slug, total);
  }

  const origin = req.headers.origin || 'https://atomatlab.com';

  const line_items = [...qtyBySlug].map(([slug, qty]) => ({
    price_data: {
      currency: 'eur',
      unit_amount: CATALOG[slug].price,
      product_data: {
        name: CATALOG[slug].name,
        description: CATALOG[slug].tagline,
        images: [`${origin}/${CATALOG[slug].image}`],
        metadata: { slug, serial: CATALOG[slug].serial },
      },
    },
    quantity: qty,
  }));

  const ship = SHIPPING[country];

  try {
    const session = await stripe.checkout.sessions.create({
      mode: 'payment',
      payment_method_types: ['card'],
      allow_promotion_codes: true,
      line_items,
      billing_address_collection: 'required',
      shipping_address_collection: { allowed_countries: [country] },
      phone_number_collection: { enabled: true },
      shipping_options: [
        {
          shipping_rate_data: {
            type: 'fixed_amount',
            fixed_amount: { amount: ship.amount, currency: 'eur' },
            display_name: `Shipping to ${ship.name}`,
            delivery_estimate: {
              minimum: { unit: 'business_day', value: 3 },
              maximum: { unit: 'business_day', value: 12 },
            },
          },
        },
      ],
      metadata: {
        shipping_country: country,
        cart: [...qtyBySlug].map(([slug, qty]) => `${slug}x${qty}`).join(','),
      },
      success_url: `${origin}/success.html`,
      cancel_url: `${origin}/cart.html`,
    });

    return res.status(200).json({ url: session.url });
  } catch (err) {
    console.error('Stripe checkout error:', err);
    return res.status(500).json({ error: 'Could not start checkout' });
  }
}
