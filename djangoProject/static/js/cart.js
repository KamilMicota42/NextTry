var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product // dataset.product or dataset.object idk
        var action = this.dataset.action
        console.log('productId: ', productId, 'action: ', action ) // only for presentation purposes

        console.log('USER: ', user) // only for presentation purposes
        if(user === 'AnonymousUser') {
            console.log('Not logged in') // only for presentation purposes
        }else{
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action){
    console.log('User is logged in, sending data...') // only for presentation purposes

    var url = '/update_item/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content_Type': 'application/json',
            'x-CSRFtoken': csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })
    .then((response) =>{
        return response.json()
    })
    .then((data) =>{
        console.log('data', data)
    })
}