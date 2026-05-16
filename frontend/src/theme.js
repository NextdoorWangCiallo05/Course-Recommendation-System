import { lightTheme } from 'naive-ui'

export const themeOverrides = {
  common: {
    primaryColor: '#2080F0',
    primaryColorHover: '#4098FC',
    primaryColorPressed: '#1060C0',
    primaryColorSuppl: '#2080F0',
    borderRadius: '8px',
    borderRadiusSmall: '6px',
    fontSize: '14px',
    fontSizeSmall: '13px',
    fontSizeMedium: '14px',
    fontSizeLarge: '16px',
    bodyColor: '#f5f7fa',
    cardColor: '#fff',
    modalColor: '#fff',
    tableColor: '#fff',
    inputColor: '#fafafa',
    tagColor: '#f0f2f5',
    dividerColor: '#e8eaed',
    hoverColor: '#f5f7fa',
  },
  Card: {
    paddingMedium: '20px',
    borderRadius: '12px',
    borderColor: 'rgba(0,0,0,0.04)',
    color: '#fff',
    boxShadow: '0 1px 4px rgba(0,0,0,0.04), 0 2px 12px rgba(0,0,0,0.04)',
  },
  Button: {
    borderRadius: '8px',
    borderRadiusSmall: '6px',
    fontSizeMedium: '14px',
    fontSizeSmall: '13px',
    heightMedium: '36px',
    heightSmall: '30px',
    paddingMedium: '0 20px',
    paddingSmall: '0 14px',
  },
  Input: {
    borderRadius: '8px',
    heightMedium: '36px',
    fontSizeMedium: '14px',
    color: '#333',
  },
  Select: {
    borderRadius: '8px',
    heightMedium: '36px',
    menuBorderRadius: '8px',
  },
  DataTable: {
    borderRadius: '10px',
    tdPaddingMedium: '10px 16px',
    thPaddingMedium: '12px 16px',
    borderColor: '#eef0f2',
    tdColor: '#fff',
    thColor: '#fafbfc',
  },
  Dialog: {
    borderRadius: '12px',
    padding: '24px',
  },
  Modal: {
    borderRadius: '12px',
  },
  Tag: {
    borderRadius: '6px',
  },
  Tabs: {
    tabPaddingMedium: '10px 0',
    tabGapMedium: '24px',
  },
  Pagination: {
    itemBorderRadius: '6px',
  },
  Dropdown: {
    borderRadius: '8px',
  },
  Menu: {
    borderRadius: '8px',
  },
  Switch: {
    railBorderRadius: '12px',
    buttonBorderRadius: '10px',
    heightMedium: '24px',
    widthMedium: '44px',
  },
  Rate: {
    starColor: '#f0c040',
  },
  Empty: {
    iconSize: '64px',
  },
  Table: {
    borderRadius: '10px',
    tdPadding: '10px 16px',
    thPadding: '12px 16px',
  },
}

export const darkThemeOverrides = {
  common: {
    bodyColor: '#141414',
    cardColor: '#1e1e1e',
    modalColor: '#1e1e1e',
    tableColor: '#1e1e1e',
    inputColor: '#2a2a2a',
    tagColor: '#2a2a2a',
    dividerColor: '#333',
    hoverColor: '#2a2a2a',
    primaryColor: '#4098FC',
    primaryColorHover: '#60A8FC',
    primaryColorPressed: '#2080F0',
    textColor: '#e8e8e8',
    textColorSecondary: '#aaa',
    placeholderColor: '#666',
  },
  Card: {
    color: '#1e1e1e',
    borderColor: 'rgba(255,255,255,0.06)',
    boxShadow: '0 1px 4px rgba(0,0,0,0.2)',
    borderRadius: '12px',
  },
  DataTable: {
    tdColor: '#1e1e1e',
    thColor: '#252525',
    borderColor: '#333',
  },
  Input: {
    color: '#e8e8e8',
    placeholderColor: '#666',
    borderColor: '#333',
    borderColorHover: '#444',
    borderColorFocus: '#4098FC',
    backgroundColor: '#2a2a2a',
  },
  Select: {
    color: '#e8e8e8',
    placeholderColor: '#666',
    borderColor: '#333',
    borderColorHover: '#444',
    borderColorFocus: '#4098FC',
    backgroundColor: '#2a2a2a',
    menuBackgroundColor: '#2a2a2a',
    optionColor: '#e8e8e8',
    optionHoverColor: '#3a3a3a',
  },
}
