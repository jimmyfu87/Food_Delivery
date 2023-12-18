function toggleLoading(show) {
    document.querySelector('.loading').style.display = show ? 'block' : 'none';
}

function submit_order() {
    let member_id = document.getElementById("member_id").textContent;
    let total_price = document.getElementById("cart_total_price").textContent;
    let payment_name = document.getElementById("payment-method").value;
    let data = { member_id: member_id, payment_name: payment_name, total_price: total_price};
    let api_url = "../order/submit_order";
    if (total_price == 0) {
        alert("購物車為空不可訂購");
        return;  
    }
    fetch(api_url, {
        method: 'POST',
        headers: new Headers({
            'Content-Type': 'application/json'
        }),
        body: JSON.stringify(data)
    }).then(response => response.json())
        .then(response => {
            if (response.success) {
                alert("訂購成功");
                location.reload();
            } else {
                alert("訂購失敗");
                location.reload();
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
function delete_all_cart_items() {
    let member_id = document.getElementById("member_id").textContent;
    let data = { member_id: member_id };
    let api_url = "../cart_item/delete_all_cart_items";
    fetch(api_url, {
        method: 'DELETE',
        headers: new Headers({
            'Content-Type': 'application/json'
        }),
        body: JSON.stringify(data)
    }).then(response => response.json())
        .then(response => {
            if (response.success) {
                alert("購物車已清空");
                location.reload();
            } else {
                alert("購物車清空失敗");
                location.reload();
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


function logout() {
    let api_url = '../user/logout';
    toggleLoading(true);
    $('#spinner-div').show();
    fetch(api_url, {
        method: 'GET',
    }).then(function (promise_result) {
        return promise_result.json();
    }).then(function (response) {
        if (response["success"] == true) {
            toggleLoading(false);
            $('#spinner-div').hide();
            alert(response['message']);
            window.location = '../Login.html';
        } else if (response["success"] == false) {
            toggleLoading(false);
            $('#spinner-div').hide();
            alert(response['message']);
            window.location = '../Login.html';
        }
    }).catch(function (err) {
        console.log(err);
    });
}

function login() {
    let member_id = document.getElementById('member_id').value;
    let member_password = document.getElementById("member_password").value;
    let data = { 'member_id': member_id, 'member_password': member_password };
    let api_url = "user/login";
    toggleLoading(true);
    $('#spinner-div').show();
    fetch(api_url, {
        method: 'POST',
        headers: new Headers({
            'Content-Type': "application/json"
        }),
        body: JSON.stringify(data)
    }).then(function (promise_result) {
        return promise_result.json();
    }).then(function (response) {
        if (response["success"] == true) {
            toggleLoading(false);
            $('#spinner-div').hide();
            window.location = '../restaurant/';
        } else if (response["success"] == false) {
            toggleLoading(false);
            $('#spinner-div').hide();
            alert(response['message']);
        }
    }).catch(function(err) {
        console.log(err);
    });
}

function add_food_tocart() {
    let cart_items = [];
    let member_id = document.getElementById("member_id").textContent;
    document.querySelectorAll('.food-row').forEach(row => {
        let food_id = row.dataset.foodId;
        let food_quantity = row.querySelector('.food-quantity-input').value;
        let food_remark = row.querySelector('.food-remark-input').value;
        if (food_quantity > 0) {
            cart_items.push({ member_id: member_id, food_id: food_id, food_quantity: food_quantity, food_remark: food_remark });
        }
    });
    if (cart_items.length === 0) {
        alert("請至少選擇一項菜");
        return;  
    }
    let data = { cart_items: cart_items };
    let api_url = "../cart_item/add_food_tocart";
    fetch(api_url, {
        method: 'POST',
        headers: new Headers({
            'Content-Type': 'application/json'
        }),
        body: JSON.stringify(data)
    }).then(response => response.json())
        .then(response => {
            if (response.success) {
                alert("已添加到購物車");
                location.reload();
            } else {
                alert("添加失敗");
                location.reload();
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function cancel_order() {
    let order_id = document.getElementById('order-id').value;
    let api_url = "../order/cancel_order?order_id=" + order_id;
    fetch(api_url, {
        method: 'PATCH',
        headers: new Headers({
            'Content-Type': 'application/json'
        }),
    }).then(response => response.json())
        .then(response => {
            if (response.success) {
                alert("取消成功");
                window.location.href = '../order'
            } else {
                alert("取消失敗");
                location.reload();
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
function register() {
    let member_id = document.getElementById('member_id').value;
    let member_password = document.getElementById("member_password").value;
    let member_email = document.getElementById("member_email").value;
    let api_url = "../user/register";
    let data = { 'member_id': member_id, 'member_password': member_password, 'member_email': member_email };
    toggleLoading(true);
    $('#spinner-div').show();
    fetch(api_url, {
        method: 'POST',
        headers: new Headers({
            'Content-Type': "application/json"
        }),
        body: JSON.stringify(data)
    }).then(function (promise_result) {
        return promise_result.json();
    }).then(function (response) {
        if (response["success"] == true) {
            toggleLoading(false);
            $('#spinner-div').hide();
            alert(response['message'])
            window.location = '../Login.html';
        } else if (response["success"] == false) {
            toggleLoading(false);
            $('#spinner-div').hide();
            alert(response['message']);
        }
    }).catch(function(err) {
        console.log(err);
    });
}


window.addEventListener('DOMContentLoaded', event => {
    // Simple-DataTables
    // https://github.com/fiduswriter/Simple-DataTables/wiki

    const datatablesSimple = document.getElementById('datatable');

});
$(document).ready(function () {
    $('#datatable').dataTable({
        "bInfo": false,
        "bPaginate": false,
        "autoWidth": false,
        "ordering": true,
        "columns": [
            { "width": "20%" },
            { "width": "20%" },
            { "width": "10%" },
            { "width": "10%" },
            { "width": "20%" },
            { "width": "10%" },
        ],
    });
});