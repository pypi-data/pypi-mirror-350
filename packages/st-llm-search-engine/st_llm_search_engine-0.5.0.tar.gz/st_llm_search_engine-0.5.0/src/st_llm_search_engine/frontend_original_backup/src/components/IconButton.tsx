// IconButton.tsx
export type IconButtonProps = {
    Icon: React.FC<React.SVGProps<SVGSVGElement>>;
    iconWidth: number | string;
    iconHeight: number | string;
    width: number | string;
    height: number | string;
    bgColor: string;
    borderRadius: number | string;
    onClick?: () => void;
    active?: boolean;
  };

  export default function IconButton({
    Icon,
    iconWidth,
    iconHeight,
    width,
    height,
    bgColor,
    borderRadius,
    onClick,
    active = false,
  }: IconButtonProps) {
    return (
      <button
        style={{
          width,
          height,
          backgroundColor: bgColor,
          borderRadius,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          padding: 0,
          border: "none",
          cursor: "pointer",
          overflow: "hidden",
          opacity: active ? 1 : 0.3,
          transition: "opacity 0.2s",
        }}
        onClick={onClick}
      >
        <div style={{ width: iconWidth, height: iconHeight, display: "flex", alignItems: "center", justifyContent: "center" }}>
          <Icon width="100%" height="100%" />
        </div>
      </button>
    );
  }
