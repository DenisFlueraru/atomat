import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).end('Method Not Allowed');
  }

  const { items } = req.body;

  if (!items || !items.length) {
    return res.status(400).json({ error: 'Cart is empty' });
  }

  try {
    const line_items = items.map(item => ({
      price_data: {
        currency: 'eur',
        product_data: {
          name: item.name,
        },
        unit_amount: item.price, // cents
      },
      quantity: item.qty,
    }));

    const session = await stripe.checkout.sessions.create({
      mode: 'payment',

      line_items,

      // 👇 THIS creates the full delivery form
      shipping_address_collection: {
        allowed_countries: [
          'RO','DE','FR','IT','ES','NL','BE','AT','PL','SE','DK','FI','GB','US'
        ],
      },

      // 👇 THIS enables shipping fees
      shipping_options: [
        { shipping_rate: 'shr_1Svh1yKCa5SQsj7OVzFU34JC' },
        { shipping_rate: 'shr_1Svh2LKCa5SQsj7OllpYbxBD' },
        { shipping_rate: 'shr_1Svh2fKCa5SQsj7OOoEmdBnj' },
        // add all shipping rate IDs here
      ],

      // 👇 Collect phone number
      phone_number_collection: {
        enabled: true,
      },

      success_url: `${req.headers.origin}/success.html`,
      cancel_url: `${req.headers.origin}/cart.html`,
    });

    res.json({ url: session.url });

  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Stripe checkout failed' });
  }
}