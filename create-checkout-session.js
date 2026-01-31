import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

// Shipping rates mapping (pre-created in Stripe)
const shippingRateIDs = {
  RO: 'shr_1Svh1yKCa5SQsj7OVzFU34JC', // Romania
  DE: 'shr_1Svh2LKCa5SQsj7OllpYbxBD', // Germany
  HU: 'shr_1Svh2fKCa5SQsj7OOoEmdBnj', // Hungary
  // Add additional countries here
};

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).end('Method Not Allowed');
  }

  const { items, country, customerEmail } = req.body;

  if (!items || !items.length) {
    return res.status(400).json({ error: 'No items in cart' });
  }

  try {
    const line_items = items.map(item => ({
      price_data: {
        currency: 'eur',
        product_data: { name: item.name },
        unit_amount: item.price, // in cents
      },
      quantity: item.qty,
    }));

    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      mode: 'payment',
      line_items,
      shipping_address_collection: {
        allowed_countries: Object.keys(shippingRateIDs),
      },
      phone_number_collection: { enabled: true },
      shipping_options: [
        { shipping_rate: shippingRateIDs[country] }
      ],
      customer_email: customerEmail || undefined,
      success_url: `${req.headers.origin}/success.html`,
      cancel_url: `${req.headers.origin}/cart.html`,
    });

    return res.status(200).json({ url: session.url });
  } catch (err) {
    console.error('Stripe checkout error:', err);
    return res.status(500).json({ error: 'Server error' });
  }
}