import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

// Shipping fees mapping in cents
const shippingRateIDs = {
  RO: 'shr_1SvgqkKCa5SQsj7OQ2VdkU0W', // Romania shipping rate
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