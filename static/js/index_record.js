
	// send date and get record
	async function send_date(){
		var date = document.getElementById('Date');
		var entry = {
			date: date.value,
			// 0:sun -> 6:sat
			day: date.valueAsDate.getDay()
		};

		let url = `${window.origin}/date`;
		let data = await restApiP(url,entry);
		document.getElementById('Day').innerHTML=data.day+"요일";
		jsonToTable(data.table);

	};
	// == end send_date ==

	// add record data
	async function addRecord(){
		var date = document.getElementById('Date');
		var table = document.getElementById('dataTableBody');
		var table_length = table.querySelectorAll('tr').length;
		var data = document.getElementById('record_data');
		var boardgame = data.querySelector("input[name='boardgame']");
		var name_list = data.querySelector("input[name='players']");

		if (date.value == "") {
			alert("날짜를 입력해 주세요.")
		}else if(boardgame.value==''|name_list==''){}
		else {
			var entry = {
				seq: table_length,
				date: date.value,
				gamename: boardgame.value,
				name_list: name_list.value
			};
			let url = `${window.origin}/addRecord`;
			let data = await restApiP(url,entry);
			boardgame.value='';
			name_list.value='';
			jsonToTable(data)
			
		}
	};
	// == end addRecord() ==

	//json to table
	function jsonToTable(json_data){
		var tablebody = document.getElementById('dataTableBody');
		var last_seq = json_data.length-1;
		var table_html = '';
		for(var i=0; i<json_data.length; i++){
			var seq = json_data[i]['seq']
			table_html += '<tr>' +
				'<td class="d-none d-md-table-cell">'+seq + '</td>'+
				'<td>'+json_data[i]['gamename']+'</td>'+
				'<td>'+json_data[i]['name_list']+'</td>' +
				'<td><button class="btn btn-sm btn-primary shadow-sm" seq='+ seq + ' onclick="deleteRecord(event)">del</button></td>';
			if(last_seq==0){ table_html += '<td></td>'
			} else if(seq == 0){
				table_html = table_html +
				'<td><button class=" btn btn-sm btn-primary shadow-sm" seq='+seq+' onclick="downRecord(event)">▼</button></td>';
			} else if(seq == last_seq){
				table_html = table_html +
				'<td><button class="btn btn-sm btn-primary shadow-sm" seq='+seq+' onclick = "upRecord(event)">▲</button></td>';
			} else {
				table_html = table_html +
				'<td><button class="btn btn-sm btn-primary shadow-sm" seq='+seq+' onclick = "upRecord(event)">▲</button>'+
				'<button class="btn btn-sm btn-primary shadow-sm" seq='+seq+' onclick="downRecord(event)">▼</button></td>';
			}
			table_html += '</tr>';
		};
		tablebody.innerHTML=table_html;
	};
	// == end jsonToTable ==

	// delete Record
	async function deleteRecord(event){
		var date = document.getElementById('Date');
		var del_seq = event.target.attributes.seq;
		var entry = {
			date: date.value,
			seq: del_seq.value
		};
		let url = `${window.origin}/delRecord`;
		let data = await restApiP(url,entry);
		jsonToTable(data)
	}
	// == end deleteRecord ==

	// up Record
	async function upRecord(e){
		var date = document.getElementById('Date');
		var seq = e.target.attributes.seq;
		console.log(seq.value,seq.value+1,seq.value-1)
		var entry = {
			date: date.value,
			seq1: seq.value,
			seq2: parseInt(seq.value)-1
		};
		console.log(entry)
		let url = `${window.origin}/swapRecord`;
		let data = await restApiP(url,entry);
		jsonToTable(data)
	}
	// == end upRecord ==
	// down Record
	async function downRecord(e){
		var date = document.getElementById('Date');
		var seq = e.target.attributes.seq;
		var entry = {
			date: date.value,
			seq1: seq.value,
			seq2: parseInt(seq.value)+1
		};
		console.log(entry)
		let url = `${window.origin}/swapRecord`;
		let data = await restApiP(url,entry);
		jsonToTable(data)

	}
	// == end downRecord ==
