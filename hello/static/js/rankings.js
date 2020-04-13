document.querySelectorAll(".upArrow").forEach(x => x.style.display = "none");

var initialCols = document.querySelectorAll("#rankingsTable > .row:first-of-type > *");
for(let i = 0; i < initialCols.length; i++) {
  let da = initialCols[i].querySelector(".downArrow");
  let ua = initialCols[i].querySelector(".upArrow");
  if(da)
    da.addEventListener('click', function() {
      da.parentElement.classList.contains("dateHeader") ? sortTableDate(i, 1) : sortTable(i, 1);
      da.style.display = "none";
      ua.style.display = "inline";
    });
  if(ua)
    ua.addEventListener('click', function() {
      ua.parentElement.classList.contains("dateHeader") ? sortTableDate(i, -1) : sortTable(i, -1);
      ua.style.display = "none";
      da.style.display = "inline";
    });
}

function sortTable(index, dir) {
  var rows = [...document.querySelectorAll("div.row.sortable")];
  rows.sort(function(a, b) {
      return dir*((a.children[index].innerHTML).localeCompare(b.children[index].innerHTML));
  });
  for (var i = 0; i < rows.length; i++) {
    document.getElementById("rankingsTable").appendChild(rows[i]);
  }
}

function sortTableDate(index, dir) {
  var rows = [...document.querySelectorAll("div.row.sortable")];
  rows.sort(function(a, b) {
      mo = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
      let aNums = a.children[index].innerHTML.replace(",", "").split(" ");
      let bNums = b.children[index].innerHTML.replace(",", "").split(" ");
      return dir*(13*32*(aNums[2] - bNums[2])
                + 32*(mo.indexOf(aNums[0]) - mo.indexOf(bNums[0]))
                + aNums[1] - bNums[1]);
  });
  for (var i = 0; i < rows.length; i++) {
    document.getElementById("rankingsTable").appendChild(rows[i]);
  }
}
