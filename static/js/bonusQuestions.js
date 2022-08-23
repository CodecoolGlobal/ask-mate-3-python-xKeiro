/* global console*/
/*jshint esversion: 6 */

// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    'use strict';
    console.log(items);
    console.log(sortField);
    console.log(sortDirection);

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    // if (sortDirection === "asc") {
    //     const firstItem = items.shift();
    //     if (firstItem) {
    //         items.push(firstItem);
    //     }
    // } else {
    //     const lastItem = items.pop();
    //     if (lastItem) {
    //         items.push(lastItem);
    //     }
    // }

    console.log(sortField);
    if (sortField === "VoteCount" || sortField === "ViewNumber") {
        if (sortDirection === "asc") {
            items.sort(function (a, b) {
                return a[sortField] - b[sortField];
            });
        } else {
            items.sort(function (a, b) {
                return b[sortField] - a[sortField];
            });
        }
    } else {
        if (sortDirection === "asc") {
            items.sort(function (a, b) {
                return a[sortField].localeCompare(b[sortField]);
            });
        } else {
            items.sort(function (a, b) {
                return b[sortField].localeCompare(a[sortField]);
            });
        }

    }
    return items;
}

// you receive an array of objects which you must filter by all its keys to have a value matching "filterValue"
function getFilteredItems(items, filterValue) {
    'use strict';
    // console.log(items);
    // console.log(filterValue);

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    // for (let i = 0; i < filterValue.length; i++) {
    //     items.pop();
    // }
    let filtered_items = [];
    if (filterValue !== "") {
        for (let i = 0; i < items.length; i++) {
            if (filterValue.length > 1 && filterValue[0] === "!") {
                if (items[i].Description.includes(filterValue.slice(1, filterValue.length)) === false && items[i].Title.includes(filterValue.slice(1, filterValue.length)) === false) {
                    filtered_items.push(items[i]);
                    console.log(items[i].Description.includes(filterValue.slice(1, filterValue.length)));
                }
            } else {
                if (items[i].Description.includes(filterValue) || items[i].Title.includes(filterValue)) {
                    filtered_items.push(items[i]);

                }
            }
        }
        return filtered_items;
    } else {
        return items;
    }

}

function toggleTheme() {
    'use strict';
    console.log("toggle theme");
    const style = document.createElement('style');
    // const backgroundColor = document.body.style.backgroundColor;
    var backgroundColor = document.body.style.background;
    console.log(backgroundColor);
    if (backgroundColor === "rgb(204, 204, 204)" || backgroundColor === "") {
        document.body.style.background = "rgb(34, 34, 34)";
        document.getElementById("content").style.color = "rgb(204, 204, 204)";
        // document.getElementById("table").style.backgroundColor = "black";
        // document.getElementById("table").style.color = "white";
    } else if (backgroundColor === "rgb(34, 34, 34)") {
        document.body.style.background = "rgb(204, 204, 204)";
        document.getElementById("content").style.color = "rgb(34, 34, 34)";
        var buttons = document.getElementsByClassName("button");
    }
    //     style.innerHTML = `
    // body {
    // background-color: black;
    // color: white;
    // }
    // table {
    // background-color: black;
    // color: white;
    // }
    // `;
    //
    // } else if (backgroundColor === "black") {
    //     style.innerHTML = `
    // body {
    // background-color: white;
    // color: black;
    // }
    // table {
    // background-color: white;
    // color: black;
    // }
    // `;
    // }
    document.head.appendChild(style);
}

function increaseFont() {
    'use strict';
    console.log("increaseFont");
    var sz = document.getElementById("content").style.fontSize;
    if (sz === '') {
        sz = 14;
    } //default font size

    var size = parseFloat(sz) * (1.2) + "px";
    document.getElementById("content").style.fontSize = size;
    // document.getElementById("table").style.fontSize = size;
}

function decreaseFont() {
    'use strict';
    console.log("decreaseFont");
    var sz = document.getElementById("content").style.fontSize;
    if (sz === '') {
        sz = 14;
    } //default font size

    var size = parseFloat(sz) / (1.2) + "px";
    document.getElementById("content").style.fontSize = size;
}
