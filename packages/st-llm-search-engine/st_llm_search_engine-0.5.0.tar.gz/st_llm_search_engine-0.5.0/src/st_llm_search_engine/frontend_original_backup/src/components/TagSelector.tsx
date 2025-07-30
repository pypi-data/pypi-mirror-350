import React from "react";
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import Chip from '@mui/material/Chip';

export type TagSelectorProps = {
  tagsList?: string[];
  value?: string[];
  onChange?: (selected: string[]) => void;
};

export default function TagSelector({ tagsList = ["學校", "政治", "媒體"], value, onChange }: TagSelectorProps) {
  // 受控模式：由外部 value/onChange 控制
  // 非受控模式：自己管理 state
  const [internal, setInternal] = React.useState<string[]>(["All"]);
  const selected = value !== undefined ? value : internal;

  const handleChange = (event: any, val: string[]) => {
    // 不做互斥，All chip 可與其他 chip 並存
    if (onChange) {
      onChange(val);
    } else {
      setInternal(val);
    }
  };

  return (
    <Autocomplete
      multiple
      options={["All", ...tagsList]}
      value={selected}
      onChange={handleChange}
      filterSelectedOptions
      disableCloseOnSelect
      getOptionLabel={option => option}
      ListboxProps={{ style: { maxHeight: 9 * 40 } }}
      renderTags={(value: string[], getTagProps) => {
        const chips = value.slice(0, 5).map((option: string, index: number) => {
          const { key, ...tagProps } = getTagProps({ index });
          return (
            <Chip
              key={option + '-' + index}
              variant="outlined"
              color="default"
              label={option}
              {...tagProps}
              style={{ background: "#28c8c8", color: "#222", border: "none" }}
            />
          );
        });
        if (value.length > 5) {
          chips.push(<span key="more" style={{ color: "#bbb", marginLeft: 8 }}>...（共{value.length}個）</span>);
        }
        return chips;
      }}
      renderInput={params => (
        <TextField
          {...params}
          variant="outlined"
          label=""
          placeholder="請輸入標籤"
          size="small"
          style={{ background: "#222", borderRadius: 12 }}
          InputLabelProps={{ style: { color: "#fff" } }}
          InputProps={{ ...params.InputProps, style: { color: "#fff" } }}
        />
      )}
      sx={{ width: "100%", marginTop: 1 }}
    />
  );
}
