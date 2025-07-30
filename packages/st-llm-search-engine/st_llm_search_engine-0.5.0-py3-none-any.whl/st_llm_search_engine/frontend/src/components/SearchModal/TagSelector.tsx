import React from "react";
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import Chip from '@mui/material/Chip';

export type TagSelectorProps = {
  tagsList?: string[];
  value?: string[];
  onChange?: (selected: string[]) => void;
  disabled?: boolean;
};

export default function TagSelector({ tagsList = ["學校", "政治", "媒體"], value, onChange, disabled = false }: TagSelectorProps) {
  // 受控模式：由外部 value/onChange 控制
  // 非受控模式：自己管理 state
  const [internal, setInternal] = React.useState<string[]>(["All"]);
  const selected = value !== undefined ? value : internal;

  // 確保始終有 "All" 選項
  React.useEffect(() => {
    // 如果是由外部控制，且沒有選擇項時，設置為 "All"
    if (value !== undefined && value.length === 0 && onChange) {
      onChange(["All"]);
    }
  }, [value, onChange]);

  const handleChange = (event: any, val: string[]) => {
    // 如果新的選擇為空，則選擇 "All"
    const newVal = val.length === 0 ? ["All"] : val;

    if (onChange) {
      onChange(newVal);
    } else {
      setInternal(newVal);
    }
  };

  return (
    <Autocomplete
      multiple
      options={["All", ...(tagsList || [])]}
      value={selected}
      onChange={handleChange}
      filterSelectedOptions
      disableCloseOnSelect
      disabled={disabled}
      getOptionLabel={option => option}
      ListboxProps={{ style: { maxHeight: 9 * 40 } }}
      renderTags={(value: string[], getTagProps) => {
        return value.map((option: string, index: number) => {
          const { key, ...tagProps } = getTagProps({ index });
          return (
            <Chip
              key={option + '-' + index}
              variant="outlined"
              color="default"
              label={option}
              {...tagProps}
              style={{
                background: "#28c8c8",
                color: "#222",
                border: "none",
                opacity: disabled ? 0.5 : 1
              }}
            />
          );
        });
      }}
      renderInput={params => (
        <TextField
          {...params}
          variant="outlined"
          label=""
          placeholder={disabled ? "" : "請輸入KOL"}
          size="small"
          style={{ background: "#222", borderRadius: 12, opacity: disabled ? 0.7 : 1 }}
          InputLabelProps={{ style: { color: "#fff" } }}
          InputProps={{
            ...params.InputProps,
            style: { color: "#fff" },
            sx: {
              '& .MuiOutlinedInput-notchedOutline': {
                borderColor: 'transparent'
              },
              '&:hover .MuiOutlinedInput-notchedOutline': {
                borderColor: disabled ? 'transparent' : '#28C8C8'
              },
              '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                borderColor: disabled ? 'transparent' : '#28C8C8'
              }
            }
          }}
          disabled={disabled}
        />
      )}
      sx={{
        width: "100%",
        marginTop: 1,
        '& .MuiAutocomplete-tag': {
          background: '#28C8C8',
          color: '#222',
          opacity: disabled ? 0.5 : 1
        },
        '& .MuiOutlinedInput-root.Mui-focused .MuiOutlinedInput-notchedOutline': {
          borderColor: disabled ? 'transparent' : '#28C8C8'
        }
      }}
    />
  );
}
