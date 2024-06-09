import * as React from 'react';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import { RequestContext } from "./Context/RequestContext";

export default function NSGNameFilter() {
const { nsgNameFilterValue, setNsgNameFilterValue } = React.useContext(RequestContext);
let [data, setData] = React.useState([]);
let [options, setOptions] = React.useState([]);

  const fetchNSG = async () => {
    let NSGFile = await fetch("./non-state-groups.json");
    let NSGJsonArray = await NSGFile.json();
    setData(NSGJsonArray);
  };

  React.useEffect(() => {
    fetchNSG();
  }, []);
  React.useEffect(()=>{
    const nsgs = data.map((nonstategroups) => ({

      label: nonstategroups.label,
      id: nonstategroups.id
    }))
    const nsgsUnique = nsgs.filter((nsg,index) => nsg.id && nsgs.findIndex(obj => obj.id == nsg.id) === index)
    console.log(nsgsUnique)
    nsgsUnique.sort((a, b) => a.label.localeCompare(b.label))
  setOptions(nsgsUnique)
  },[data]
  );
  return (
    <Autocomplete
      multiple
      disablePortal
      id="combo-box-NSG"
      options={options}
      value={nsgNameFilterValue}
      onChange={(event, newValue)=>{
      setNsgNameFilterValue(newValue);

      }}
      getOptionLabel={(option)=>option.label}
      sx={{ width: 300 ,marginTop: '10px'}}
      renderInput={(params) => <TextField {...params} label="Name" />}
    />
  );
}