function addRow(){
var tableid=document.getElementById('ingredients')
var table=tableid.getElementsByTagName('table')[0];
var row=table.insertRow(table.rows.length);
var cell1=row.insertCell(0);
var cell2=row.insertCell(1);
var cell3=row.insertCell(2);
var cell4=row.insertCell(3);
var numid=table.rows.length-1
cell1.innerHTML="<input type='text' name='amout"+numid+"'>";
cell2.innerHTML="<input type='text' name='amoutUnit"+numid+"' placeholder='cdta/gr/ml...'>";
cell3.innerHTML="<input type='text' name='ingredients"+numid+"'>";
cell4.innerHTML="<input type='text' name='notes"+numid+"'>";
var counterRows = document.getElementById('amoutRows')
counterRows.innerHTML=table.rows.length;
}