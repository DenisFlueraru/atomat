const CART_KEY = 'atomat_cart';

function getCart() {
  return JSON.parse(localStorage.getItem(CART_KEY)) || [];
}

function saveCart(cart) {
  localStorage.setItem(CART_KEY, JSON.stringify(cart));
}

function addToCart(product) {
  const cart = getCart();
  const existing = cart.find(i => i.id === product.id);

  if (existing) {
    existing.qty += 1;
  } else {
    cart.push({ ...product, qty: 1 });
  }

  saveCart(cart);
  updateCartUI();
}

function clearCart() {
  localStorage.removeItem(CART_KEY);
  updateCartUI();
}

function getCartCount() {
  return getCart().reduce((sum, i) => sum + i.qty, 0);
}

function updateCartUI() {
  const count = getCartCount();
  document.querySelectorAll('#cart-count').forEach(el => {
    el.textContent = `(${count})`;
    el.style.display = count > 0 ? 'inline' : 'none';
  });

  document.querySelectorAll('#cart-dot').forEach(el => {
    el.style.display = count > 0 ? 'block' : 'none';
  });
}

document.addEventListener('DOMContentLoaded', updateCartUI);