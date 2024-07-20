// Esto es la configuracion para los botones
var updateBtns = document.getElementsByClassName('update-cart')

for(i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'action:', action)

		console.log('USER:', user)
		if(user == 'AnonymousUser'){
			addCookieItem(productId, action)
		}else{
			updateUserOrder(productId, action)
		}
	})
}

function addCookieItem(productId, action){
	console.log('Not logged in')

	if(action == 'add'){
		if(cart[productId] == undefined){
			cart[productId] = {'quantity':1}
		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if(action == 'remove'){
		cart[productId]['quantity'] -= 1

		if(cart[productId]['quantity'] <= 0){
			console.log('Remove item')
			delete cart[productId];
		}
	}

	console.log('Cart:', cart)
	document.cookie = 'cart=' + JSON.stringify(cart) + ";domain;path=/"
	
	location.reload()
}

function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})
		})

		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    console.log('data:', data)
			location.reload()
		});
}


// Aca para el view por producto
const imgs = document.querySelectorAll('.img-select a');
const imgBtns = [...imgs];
let imgId = 1;

imgBtns.forEach((imgItem) => {
    imgItem.addEventListener('click', (event) => {
        event.preventDefault();
        imgId = imgItem.dataset.id;
        slideImage();
    });
});

function slideImage(){
    const displayWidth = document.querySelector('.img-showcase img:first-child').clientWidth;

    document.querySelector('.img-showcase').style.transform = `translateX(${- (imgId - 1) * displayWidth}px)`;
}

window.addEventListener('resize', slideImage);
