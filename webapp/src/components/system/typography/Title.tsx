import clsx from "clsx";
import type { CSSProperties } from "react";
import type { HeadingLevel } from "./types";
import styles from "./typography.module.css";

export interface TitleProps {
  level: HeadingLevel;
  children: React.ReactNode;
  className?: string;
  style?: CSSProperties;
}

export function Title({ level, children, className, ...htmlProps }: TitleProps) {
  const Element = level;

  return (
    <Element
      className={clsx(styles.title, styles[`headin_level_${level}`], className)}
      {...htmlProps}
    >
      {children}
    </Element>
  );
}
