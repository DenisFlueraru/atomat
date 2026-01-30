/* ================= CART STATE ================= */

// Get cart from localStorage
function getCart() {
  return JSON.parse(localStorage.getItem('cart')) || [];
}

// Save cart
function saveCart(cart) {
  localStorage.setItem('cart', JSON.stringify(cart));
}

// Add item to cart
function addToCart(product) {
  const cart = getCart();

  const existing = cart.find(item => item.id === product.id);
  if (existing) {
    existing.qty += 1;
  } else {
    cart.push({ ...product, qty: 1 });
  }

  saveCart(cart);
  updateCartCount();
}

// Count total items
function getCartCount() {
  return getCart().reduce((sum, item) => sum + item.qty, 0);
}

// Update cart badge (desktop + mobile)
function updateCartCount() {
  const count = getCartCount();

  document.querySelectorAll('.dot').forEach(dot => {
    if (count > 0) {
      dot.style.display = 'inline-flex';
      dot.textContent = count;
    } else {
      dot.style.display = 'none';
    }
  });
}

// Run on page load
document.addEventListener('DOMContentLoaded', updateCartCount);