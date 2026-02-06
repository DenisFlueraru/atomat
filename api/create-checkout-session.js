import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

// Dummy shipping rate to display "Shipping: Already calculated at checkout"
// Create one shipping rate in Stripe Dashboard called "Shipping (calculated)" and copy its ID here
const SHIPPING_RATE_ID = 'shr_1Sxjj1KCa5SQsj7OpqmXn5la';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).end('Method Not Allowed');
  }

  const { items, country } = req.body;

  if (!items || !items.length) {
    return res.status(400).json({ error: 'Cart is empty' });
  }

  try {
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      mode: 'payment',
      line_items: items, // includes shipping as a separate product already
      shipping_address_collection: {
        allowed_countries: [country], // only allow the selected country
      },
      phone_number_collection: { enabled: true },
      shipping_options: [
        { shipping_rate: SHIPPING_RATE_ID } // dummy rate just to show "Shipping: calculated"
      ],
      metadata: { shipping_country: country },
      success_url: `${req.headers.origin}/success.html`,
      cancel_url: `${req.headers.origin}/cart.html`,
    });

    return res.status(200).json({ url: session.url });
  } catch (err) {
    console.error('Stripe checkout error:', err);
    return res.status(500).json({ error: 'Server error' });
  }
}