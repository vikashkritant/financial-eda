# src/data_cleaner.py

import pandas as pd


def clean_financials(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the S&P 500 financials dataframe.
    Steps:
      1. Drop rows with missing core price data
      2. Fill Dividend Yield nulls with 0
      3. Fill remaining numeric nulls with median
    Returns cleaned dataframe.
    """

    # Step 1 — Drop rows where core price columns are missing
    core_cols = ["Price", "Market Cap", "52 Week Low", "52 Week High"]
    df = df.dropna(subset=core_cols)

    # Step 2 — No dividend = 0, not missing
    df["Dividend Yield"] = df["Dividend Yield"].fillna(0)

    # Step 3 — Fill remaining numeric columns with median
    cols_to_fill = ["Price/Earnings", "Earnings/Share", "EBITDA", 
                    "Price/Sales", "Price/Book"]
    for col in cols_to_fill:
        df[col] = df[col].fillna(df[col].median())
    
    # Add broad sector mapping
    df = map_to_broad_sector(df)

    return df

# src/data_cleaner.py — add this function

def map_to_broad_sector(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a 'Broad Sector' column mapping granular sub-sectors
    to the 11 standard GICS broad sectors.
    Original 'Sector' column is preserved.
    """

    mapping = {
        # ── Information Technology ─────────────────────────────────────────
        "Application Software":                        "Information Technology",
        "Systems Software":                            "Information Technology",
        "Technology Hardware, Storage & Peripherals":  "Information Technology",
        "Semiconductors":                              "Information Technology",
        "Semiconductor Materials & Equipment":         "Information Technology",
        "IT Consulting & Other Services":              "Information Technology",
        "Data Processing & Outsourced Services":       "Information Technology",
        "Internet Services & Infrastructure":          "Information Technology",
        "Electronic Equipment & Instruments":          "Information Technology",
        "Electronic Components":                       "Information Technology",
        "Electronic Manufacturing Services":           "Information Technology",
        "Technology Distributors":                     "Information Technology",

        # ── Health Care ────────────────────────────────────────────────────
        "Health Care Equipment":                       "Health Care",
        "Health Care Supplies":                        "Health Care",
        "Health Care Services":                        "Health Care",
        "Health Care Facilities":                      "Health Care",
        "Health Care Distributors":                    "Health Care",
        "Health Care Technology":                      "Health Care",
        "Biotechnology":                               "Health Care",
        "Pharmaceuticals":                             "Health Care",
        "Life Sciences Tools & Services":              "Health Care",
        "Managed Health Care":                         "Health Care",
        "Health Care REITs":                           "Health Care",

        # ── Financials ─────────────────────────────────────────────────────
        "Diversified Banks":                           "Financials",
        "Regional Banks":                              "Financials",
        "Investment Banking & Brokerage":              "Financials",
        "Asset Management & Custody Banks":            "Financials",
        "Insurance Brokers":                           "Financials",
        "Life & Health Insurance":                     "Financials",
        "Multi-line Insurance":                        "Financials",
        "Property & Casualty Insurance":               "Financials",
        "Reinsurance":                                 "Financials",
        "Financial Exchanges & Data":                  "Financials",
        "Consumer Finance":                            "Financials",
        "Transaction & Payment Processing Services":   "Financials",
        "Multi-Sector Holdings":                       "Financials",

        # ── Consumer Discretionary ─────────────────────────────────────────
        "Automobile Manufacturers":                    "Consumer Discretionary",
        "Automotive Parts & Equipment":                "Consumer Discretionary",
        "Automotive Retail":                           "Consumer Discretionary",
        "Apparel Retail":                              "Consumer Discretionary",
        "Apparel, Accessories & Luxury Goods":         "Consumer Discretionary",
        "Footwear":                                    "Consumer Discretionary",
        "Broadline Retail":                            "Consumer Discretionary",
        "Computer & Electronics Retail":               "Consumer Discretionary",
        "Home Improvement Retail":                     "Consumer Discretionary",
        "Other Specialty Retail":                      "Consumer Discretionary",
        "Homebuilding":                                "Consumer Discretionary",
        "Home Furnishings":                            "Consumer Discretionary",
        "Leisure Products":                            "Consumer Discretionary",
        "Hotels, Resorts & Cruise Lines":              "Consumer Discretionary",
        "Restaurants":                                 "Consumer Discretionary",
        "Movies & Entertainment":                      "Consumer Discretionary",
        "Interactive Home Entertainment":              "Consumer Discretionary",
        "Casinos & Gaming":                            "Consumer Discretionary",
        "Drug Retail":                                 "Consumer Discretionary",
        "Consumer Electronics":                        "Consumer Discretionary",

        # ── Consumer Staples ───────────────────────────────────────────────
        "Packaged Foods & Meats":                      "Consumer Staples",
        "Soft Drinks & Non-alcoholic Beverages":       "Consumer Staples",
        "Tobacco":                                     "Consumer Staples",
        "Household Products":                          "Consumer Staples",
        "Personal Care Products":                      "Consumer Staples",
        "Food Retail":                                 "Consumer Staples",
        "Food Distributors":                           "Consumer Staples",
        "Consumer Staples Merchandise Retail":         "Consumer Staples",
        "Brewers":                                     "Consumer Staples",
        "Distillers & Vintners":                       "Consumer Staples",
        "Agricultural Products & Services":            "Consumer Staples",

        # ── Energy ────────────────────────────────────────────────────────
        "Integrated Oil & Gas":                        "Energy",
        "Oil & Gas Exploration & Production":          "Energy",
        "Oil & Gas Refining & Marketing":              "Energy",
        "Oil & Gas Equipment & Services":              "Energy",
        "Oil & Gas Storage & Transportation":          "Energy",
        "Independent Power Producers & Energy Traders":"Energy",
        "Coal & Consumable Fuels":                     "Energy",

        # ── Industrials ───────────────────────────────────────────────────
        "Aerospace & Defense":                         "Industrials",
        "Industrial Machinery & Supplies & Components":"Industrials",
        "Construction Machinery & Heavy Transportation Equipment": "Industrials",
        "Agricultural & Farm Machinery":               "Industrials",
        "Heavy Electrical Equipment":                  "Industrials",
        "Building Products":                           "Industrials",
        "Construction & Engineering":                  "Industrials",
        "Air Freight & Logistics":                     "Industrials",
        "Cargo Ground Transportation":                 "Industrials",
        "Passenger Airlines":                          "Industrials",
        "Passenger Ground Transportation":             "Industrials",
        "Rail Transportation":                         "Industrials",
        "Trading Companies & Distributors":            "Industrials",
        "Distributors":                                "Industrials",
        "Industrial Conglomerates":                    "Industrials",
        "Environmental & Facilities Services":         "Industrials",
        "Diversified Support Services":                "Industrials",
        "Human Resource & Employment Services":        "Industrials",
        "Research & Consulting Services":              "Industrials",
        "Advertising":                                 "Industrials",
        "Publishing":                                  "Industrials",
        "Broadcasting":                                "Industrials",

        # ── Materials ─────────────────────────────────────────────────────
        "Specialty Chemicals":                         "Materials",
        "Commodity Chemicals":                         "Materials",
        "Fertilizers & Agricultural Chemicals":        "Materials",
        "Industrial Gases":                            "Materials",
        "Construction Materials":                      "Materials",
        "Metal, Glass & Plastic Containers":           "Materials",
        "Paper & Plastic Packaging Products & Materials": "Materials",
        "Steel":                                       "Materials",
        "Copper":                                      "Materials",
        "Gold":                                        "Materials",

        # ── Real Estate ───────────────────────────────────────────────────
        "Multi-Family Residential REITs":              "Real Estate",
        "Single-Family Residential REITs":             "Real Estate",
        "Office REITs":                                "Real Estate",
        "Retail REITs":                                "Real Estate",
        "Industrial REITs":                            "Real Estate",
        "Hotel & Resort REITs":                        "Real Estate",
        "Self-Storage REITs":                          "Real Estate",
        "Health Care REITs":                           "Real Estate",
        "Data Center REITs":                           "Real Estate",
        "Timber REITs":                                "Real Estate",
        "Other Specialized REITs":                     "Real Estate",
        "Real Estate Services":                        "Real Estate",

        # ── Utilities ─────────────────────────────────────────────────────
        "Electric Utilities":                          "Utilities",
        "Gas Utilities":                               "Utilities",
        "Multi-Utilities":                             "Utilities",
        "Water Utilities":                             "Utilities",

        # ── Communication Services ────────────────────────────────────────
        "Interactive Media & Services":                "Communication Services",
        "Integrated Telecommunication Services":       "Communication Services",
        "Wireless Telecommunication Services":         "Communication Services",
        "Telecom Tower REITs":                         "Communication Services",
        "Cable & Satellite":                           "Communication Services",
        "Electrical Components & Equipment":           "Communication Services",
        "Communications Equipment":                    "Communication Services",
    }

    df["Broad Sector"] = df["Sector"].map(mapping)

    # Safety check — flag any unmapped sub-sectors
    unmapped = df[df["Broad Sector"].isna()]["Sector"].unique()
    if len(unmapped) > 0:
        print(f"WARNING: {len(unmapped)} unmapped sub-sectors found:")
        for s in unmapped:
            print(f"  - {s}")

    return df