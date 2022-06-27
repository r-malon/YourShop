"use strict";

const nav_search = document.getElementById("nav_search");
const more = document.getElementById("more");
const per_page = document.getElementById("per_page");
const order_el = document.getElementById("order");
const items_div = document.getElementById("items");
const alerts_div = document.getElementById("alerts");
let alert_id = 0;
let timeout = null;
let start = 0;


window.onload = () => {
	start = +per_page.value;
	fetch(`/items?limit=${start}`)
		.then(response => response.json())
		.then(
			data => parseItems(data, "beforeend", true)
		);
}


nav_search.addEventListener("keyup", (e) => {
	clearTimeout(timeout);
//	hacky mobile fix
	if (!checkCode(e.keyCode) && e.keyCode != undefined && e.keyCode != 229) return;
	updateItemsURL(true);

	timeout = setTimeout(() => {
		fetch(localStorage.itemsURL)
		.then(response => response.json())
		.then(
			data => parseItems(data, "beforeend", true)
		);
	}, 400);
});


more.addEventListener("click", (e) => {
	let no_results = document.getElementById("no_results");
	if (no_results) no_results.remove();

	updateItemsURL(false);

	fetch(localStorage.itemsURL)
	.then(response => response.json())
	.then(
		data => parseItems(data, "beforeend", false)
	);
	start += +per_page.value;	// to int
});


function updateItemsURL(to_search) {
	localStorage.itemsURL = "/items?" + new URLSearchParams({
		search: to_search ? nav_search.value : '', 
		order: order_el.value, 
		start: to_search ? '' : start, 
		limit: per_page.value
	});
}


function parseItems(data, mode, clear) {
	if (clear) {
		items_div.textContent = "";
	}
	if (!data?.length) {
		items_div.insertAdjacentHTML(
			"beforeend", 
			"<h5 id='no_results' class='fw-bold text-center'>NADA ENCONTRADO</h5>"
		);
		return;
	}
	data.forEach((item) => {
		let item_template = `
		<div class="col-md-4 item_card">
			<div class="card rounded shadow-sm">
				<img src="static/uploads/${item.id}.png" class="card-img-top">
				<ul class="list-group list-group-flush">
					<li class="list-group-item">${item.desc}</li>
					<li class="list-group-item">Quantidade: ${item.qty}</li>
					<li class="list-group-item">Preço: R$ ${item.price}</li>
					<li class="list-group-item">
						<div class="wrap" data-id="${item.id}" onclick="delItem(this)">
							<object data="static/trash.svg" class="red"></object>
						</div>
					</li>
				</ul>
			</div>
		</div>
		`
		items_div.insertAdjacentHTML(mode, item_template);
	});
}


function delItem(item) {
	fetch(`/items/${item.getAttribute("data-id")}`, {
		method: "DELETE"
	})
	.then(response => response.json())
	.then(data => putAlert(data))
	.then(
		item.parentNode.parentNode.parentNode.parentNode.remove()
	);
}


function putAlert(data) {
	let alert_template = `
	<div id="alert${alert_id}" class="alert alert-${data.category} alert-dismissible fade show" role="alert">
		<span>${data.message}</span>
		<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
	</div>
	`
	alerts_div.insertAdjacentHTML("beforeend", alert_template);
	setTimeout(function() {
		document.getElementById(`alert${alert_id}`).remove();
		alert_id++;
	}, 2000);
}


function checkCode(keycode) {
	let valid = 
			(keycode > 47 && keycode < 58)   ||
			(keycode > 64 && keycode < 91)   ||
			(keycode > 95 && keycode < 112)  ||
			(keycode > 185 && keycode < 193) ||
			(keycode > 218 && keycode < 223);
	return valid;
}

const sort_by = (field, reverse, primer) => {
	const key = primer ?
		function(x) {
			return primer(x[field])
		} :
		function(x) {
			return x[field]
		};
	reverse = !reverse ? 1 : -1;

	return function(a, b) {
		return a = key(a), b = key(b), reverse * ((a > b) - (b > a));
	}
}
