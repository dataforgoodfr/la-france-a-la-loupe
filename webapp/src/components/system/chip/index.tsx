import { clsx } from "clsx";
import type { ButtonHTMLAttributes } from "react";
import styles from "./chip.module.css";

export interface ChipProps extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "aria-pressed"> {
  selected?: boolean;

  "data-hover"?: boolean;
  "data-active"?: boolean;
  "data-focus-visible"?: boolean;
}

export function Chip({
  selected = false,
  children,
  type = "button",
  className,
  ...htmlProps
}: ChipProps) {
  return (
    <button
      type={type}
      aria-pressed={selected}
      className={clsx(styles.chip, className)}
      {...htmlProps}
    >
      {children}
    </button>
  );
}
