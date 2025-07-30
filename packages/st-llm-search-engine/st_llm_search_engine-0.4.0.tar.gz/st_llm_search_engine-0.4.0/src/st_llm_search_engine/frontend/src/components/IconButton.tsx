import React from 'react';

interface IconButtonProps {
  Icon: React.FC<React.SVGProps<SVGSVGElement>>;
  iconWidth: number;
  iconHeight: number;
  width: string | number;
  height: number;
  bgColor: string;
  borderRadius: string;
  active: boolean;
  onClick: () => void;
}

const IconButton: React.FC<IconButtonProps> = ({
  Icon,
  iconWidth,
  iconHeight,
  width,
  height,
  bgColor,
  borderRadius,
  active,
  onClick
}) => {
  return (
    <button
      onClick={onClick}
      style={{
        width,
        height,
        background: active ? '#444444' : bgColor,
        border: 'none',
        borderRadius,
        cursor: 'pointer',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        transition: 'background-color 0.2s',
        padding: 0,
      }}
    >
      <Icon
        width={iconWidth}
        height={iconHeight}
        style={{
          opacity: active ? 1 : 0.6,
          transition: 'opacity 0.2s',
        }}
      />
    </button>
  );
};

export default IconButton;
