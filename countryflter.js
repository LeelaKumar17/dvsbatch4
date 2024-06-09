import React, {useContext} from "react";
import { RequestContext } from"./context/RequestContext";
Import Autocomplete from "@mui/material/Autocomplete";
import TextField from "@mui/material/TextField";
import {Tooltip } from "@mui/material";
Import (ListitemText } from "@mui/material";

export default function CountryFilter() {
const { countryFilterValue, setCountryFilterValue, countryFilterOptions } =
useContext(RequestContext);
const getoptionLabel = (_option) => {

let option = countryFilterOptions.find((o) => o.id===_option.id); 
if (option) {

return option.label+" (" + option.count + ")";
}
};

return ( 
<Autocomplete
multiple
id="tags-standard"
options={
countryFilterValue.length >0
? countryFilterOptions.filter(
(a) => !countryFilterValue.map((b) => b.id).includes (a.id)
)
: countryFilterOptions
}
value = {countryFilterValue} 
getoptionLabel={getoptionLabel}
onchange={(event, newvalue) => {
setCountryFilterValue(newWalue); }}
sx={{

width: 250,
marginTop: "10px",
marginLeft: "auto",
marginRight: "auto",
}}
renderInput={(params)=>(
    <TextField
    {...params}
    label="classification"
    placeholder="classification"
    />
)}
/>
);
}
