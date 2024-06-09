import * as React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import ReactDOM from "react-dom";
import { RequestContext } from "./Context/RequestContext";

export default function NSGTable() {
  let [data, setData] = React.useState([]);
  let [filteredData, setFilteredData] = React.useState([]);

  const { nsgNameFilterValue,nsgCountryFilterValue,nsgEntityStatusFilterValue,
    nsgGroupObjectiveFilterValue,nsgGroupScopeFilterValue,nsgOrganizationTypeFilterValue } = React.useContext(RequestContext);
 

  React.useEffect(()=>{
    if(data.length>0){
    let query = false

    if (nsgNameFilterValue.length>0){
      query = true
    }
    if (nsgCountryFilterValue.length>0){
      query = true
    }
    if (nsgEntityStatusFilterValue.length>0){
      query = true
    }
    if (nsgGroupObjectiveFilterValue.length>0){
      query = true
    }
    if (nsgGroupScopeFilterValue.length>0){
      query = true
    }
    if (nsgOrganizationTypeFilterValue.length>0){
      query = true
    }
    if (query==true){
      let dataReplica = data;
      if (nsgNameFilterValue.length>0){
        dataReplica = dataReplica.filter((a) =>
            nsgNameFilterValue
              .map((a) => a.label)
              .includes(a.label)
          );
      }
        if (nsgCountryFilterValue.length>0){
          dataReplica = dataReplica.filter((a) =>
              nsgCountryFilterValue
                .map((b) => b.label)
                .includes(a.countryOfOrigin)
            );
        }
          if (nsgEntityStatusFilterValue.length>0){
            dataReplica = dataReplica.filter((a) =>
            nsgEntityStatusFilterValue
                  .map((b) => b.label)
                  .includes(a.entityStatus)
              );
          }
          if (nsgGroupObjectiveFilterValue.length>0){
            dataReplica = dataReplica.filter((a) =>
            nsgGroupObjectiveFilterValue
                  .map((b) => b.label)
                  .includes(a.groupObjective)
              );
          }
          if (nsgGroupScopeFilterValue.length>0){
            dataReplica = dataReplica.filter((a) =>
            nsgGroupScopeFilterValue
                  .map((b) => b.label)
                  .includes(a.groupScope)
              );
          }
          if (nsgOrganizationTypeFilterValue.length>0){
            dataReplica = dataReplica.filter((a) =>
            nsgOrganizationTypeFilterValue
                  .map((b) => b.label)
                  .includes(a.organizationType)
              );
          }
      setFilteredData(dataReplica)

    }else{
      setFilteredData(data);
    }
  }

  },[nsgNameFilterValue,nsgCountryFilterValue,nsgEntityStatusFilterValue,nsgGroupObjectiveFilterValue,
    nsgGroupScopeFilterValue,nsgOrganizationTypeFilterValue, data])


  const fetchNSG = async () => {
    let NSGFile = await fetch("./non-state-groups.json");
    let NSGJsonArray = await NSGFile.json();
    let rows = NSGJsonArray.filter(n=>n.body).map((nonstategroups) => ({
      label : nonstategroups.label,
      countryOfOrigin : nonstategroups.countryOfOrigin?.label,
      entityStatus : nonstategroups.entityStatus?.label,
      groupObjective : nonstategroups.groupObjective?.label,
      groupScope : nonstategroups.groupScope?.label,
      organizationType : nonstategroups.organizationType?.label,
      id : nonstategroups.id,
      body: nonstategroups.body,

    }
      ));
      rows.sort((a, b) => a.label.localeCompare(b.label))
    setData(rows);
    setFilteredData(rows);
  };

  React.useEffect(() => {
    fetchNSG();
  }, []);

  const handleRowClick = (params) => {
    if (params.row.body) {
      const popupWindow = window.open("", "", "height: 500;width:500");
      popupWindow.document.head.innerHTML = window.document.head.innerHTML;
      popupWindow.document.title = params.row.label;

      const htmlDom = new DOMParser().parseFromString(
        params.row.body,
        "text/html"
      );
      htmlDom.querySelectorAll("data").forEach((e) => {
        let image = document.createElement("img");
        let caption = e.getAttribute("data-caption");
        let image_name = e.getAttribute("value").split("/").slice(-1)[0];

        image.src = `./assets/images/${image_name}.jpg`;
        image.style = "max-width:400px;";
        let figure = document.createElement("figure");
        figure.append(image);
        let new_div = document.createElement("figcaption");
        new_div.innerHTML = caption;
        figure.append(new_div);
        e.replaceWith(figure);
      });

      var result = htmlDom.body.innerHTML;

      ReactDOM.render(

        <>
          <div
            style={{
              padding: "15px",
              borderColor: "white",
              borderStyle: "groove",
              borderWidth: "3px",
              borderRadius: "10px",
            }}
            className={"profile"}
          >
            <h1 id="home">{params.row.label}</h1>
            <div
              style={{ textAlign: "justify" }}
              dangerouslySetInnerHTML={{ __html: result }}
            ></div>
          </div>
        </>,
        popupWindow.document.body
      );
    }
  };

const columns = [
  { field: 'label', headerName: <b>Name</b>, width: 500 },
  { field: 'countryOfOrigin', headerName: <b>Country Of Origin</b>, width: 250 },
  { field: 'entityStatus', headerName: <b>Entity Status</b>, width: 200 },
  { field: 'groupObjective', headerName: <b>Group Objective</b>, width: 200 },
  { field: 'groupScope', headerName: <b>Group Scope</b>, width: 200 },
  { field: 'organizationType', headerName: <b>Organization Type</b>, width: 200 },
  { field: 'id', headerName: 'id', width: 400 },
  { field: "body", headerName: "body", width: 130 }
 
 
];

  return (
   
    <div style={{ height: '80vh', width: '100%' }}>
      <DataGrid
        rows={filteredData}
        columns={columns}
        onRowClick={handleRowClick}
        initialState={{
          pagination: {
            paginationModel: { page: 0, pageSize: 100 },
          },
          columns: {
            columnVisibilityModel: {
              // Hide columns status and traderName, the other columns will remain visible
              id: false,
              body: false,
            },
          },
        }}
        pageSizeOptions={[25, 50, 100]}
       
      />
    </div>
   
  );
}
