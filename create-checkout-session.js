import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

// Shipping fees mapping in cents
const shippingFees = {
  RO: 500,
  DE: 1200,
  HU: 1200,
  GB: 2600,
  AT: 1300,
  BE: 2200,
  FR: 1400,
  PL: 1200,
  ES: 1500,
  LU: 2000,
  DK: 2000,
  CZ: 1000,
  SK: 1000,
  HR: 1000,
  CY: 1000,
  EE: 1500,
  LV: 1500,
  FI: 4000,
  IE: 1800,
  LT: 1500,
  NL: 1700,
  PT: 1400,
  SI: 1000,
  SE: 2500,
  CH: 2500,
  IT: 1400,
  BG: 1000,
  GR: 1000,
  US: 2500,
};

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).end('Method Not Allowed');
  }

  const { items, country } = req.body;

  if (!items || !items.length) {
    return res.status(400).json({ error: 'No items in cart' });
  }

  const shippingFee = shippingFees[country] || 0;

  try {
    const line_items = items.map(item => ({
      price_data: {
        currency: 'eur',
        product_data: {
          name: item.name,
        },
        unit_amount: item.price, // must be in cents
      },
      quantity: item.qty,
    }));

    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      mode: 'payment',
      line_items,
      shipping_address_collection: {
        allowed_countries: Object.keys(shippingFees),
      },
      shipping_options: shippingFee ? [{
        shipping_rate_data: {
          type: 'fixed_amount',
          fixed_amount: { amount: shippingFee, currency: 'eur' },
          display_name: 'Shipping',
        }
      }] : [],
      success_url: `${req.headers.origin}/success.html`,
      cancel_url: `${req.headers.origin}/cart.html`,
    });

    return res.status(200).json({ url: session.url });
  } catch (err) {
    console.error('Stripe checkout error:', err);
    return res.status(500).json({ error: 'Server error' });
  }
}