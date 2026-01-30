function getCart(){
  return JSON.parse(localStorage.getItem('cart') || '[]');
}

function saveCart(cart){
  localStorage.setItem('cart', JSON.stringify(cart));
}

function addToCart(item){
  const cart = getCart();
  const existing = cart.find(p => p.id === item.id);

  if(existing){
    existing.qty += 1;
  } else {
    cart.push({...item, qty:1});
  }

  saveCart(cart);
  updateCartDot();
}

function updateCartDot(){
  const cart = getCart();

  const desktopDot = document.querySelector('.cart.desktop-cart .dot');
  if(desktopDot){
    desktopDot.style.display = cart.length ? 'inline-block' : 'none';
  }

  const mobileDot = document.querySelector('.cart.mobile-cart .dot');
  if(mobileDot){
    mobileDot.style.display = cart.length ? 'inline-block' : 'none';
  }
}

document.addEventListener('DOMContentLoaded', updateCartDot);