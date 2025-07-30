import argparse
import logging
from datetime import datetime
from typing import Dict, Any

from longport.openapi import Config, QuoteContext, Period, AdjustType, Market, SecurityListCategory, CalcIndex
from mcp.server import FastMCP

mcp = FastMCP("longport-stock", settings={"log_level": "DEBUG"})


def create_quote_context(app_key: str, app_secret: str, access_token: str, region: str = "cn",
                         enable_overnight: bool = True):
    """
    Create QuoteContext with provided credentials
    
    Args:
        app_key: LongPort APP key
        app_secret: LongPort APP secret
        access_token: LongPort access token
        region: API region, default "cn"
        enable_overnight: Enable overnight quotes, default True
        
    Returns:
        QuoteContext instance
    """
    import os

    # Save original file descriptors
    stdout_fd = os.dup(1)
    stderr_fd = os.dup(2)
    
    # Open devnull and get its file descriptor
    devnull = open(os.devnull, 'w')
    devnull_fd = devnull.fileno()
    
    try:
        # Redirect at file descriptor level
        os.dup2(devnull_fd, 1)  # stdout
        os.dup2(devnull_fd, 2)  # stderr
        
        config = Config(
            app_key=app_key,
            app_secret=app_secret,
            access_token=access_token,
            enable_overnight=enable_overnight,
            log_path="/tmp/longport.log",
        )
        return QuoteContext(config)
    finally:
        # Restore original file descriptors
        os.dup2(stdout_fd, 1)
        os.dup2(stderr_fd, 2)
        
        # Clean up
        os.close(stdout_fd)
        os.close(stderr_fd)
        devnull.close()

@mcp.tool()
def get_quote(symbol: str) -> Dict[str, Any]:
    """
    Get real-time quote for a security
    
    Args:
        symbol: Security code in ticker.region format, e.g. 700.HK
        
    Returns:
        Dict containing real-time quote data including last price, volume etc.
    """
    try:
        resp = ctx.quote([symbol])

        if not resp:
            return {"error": "No data returned"}

        quote_data = resp[0]
        return {
            "symbol": quote_data.symbol,
            "last_price": quote_data.last_done,
            "prev_close": quote_data.prev_close,
            "open": quote_data.open,
            "high": quote_data.high,
            "low": quote_data.low,
            "volume": quote_data.volume,
            "turnover": quote_data.turnover,
            "timestamp": quote_data.timestamp,
            "trade_status": quote_data.trade_status
        }

    except Exception as e:
        logging.error(f"Error getting quote for {symbol}: {str(e)}")
        return {"error": str(e)}


@mcp.tool()
def get_static_info(symbol: str) -> Dict[str, Any]:
    """
    Get basic information for a security
    
    Args:
        symbol: Security code in ticker.region format, e.g. 700.HK
        
    Returns:
        Dict containing static information including:
        - Company names (English, Simplified Chinese, Traditional Chinese)
        - Exchange
        - Currency
        - Lot size
        - Total shares
        - Circulating shares
        - EPS
        - Dividend yield
        etc.
    """
    try:
        resp = ctx.static_info([symbol])

        if not resp:
            return {"error": "No data returned"}

        static_data = resp[0]
        return {
            "symbol": static_data.symbol,
            "name_en": static_data.name_en,
            "name_cn": static_data.name_cn,
            "name_hk": static_data.name_hk,
            "exchange": static_data.exchange,
            "currency": static_data.currency,
            "lot_size": static_data.lot_size,
            "total_shares": static_data.total_shares,
            "circulating_shares": static_data.circulating_shares,
            "hk_shares": static_data.hk_shares,
            "eps": static_data.eps,
            "eps_ttm": static_data.eps_ttm,
            "bps": static_data.bps,
            "dividend_yield": static_data.dividend_yield,
            "stock_derivatives": static_data.stock_derivatives,
            "board": static_data.board
        }

    except Exception as e:
        logging.error(f"Error getting static info for {symbol}: {str(e)}")
        return {"error": str(e)}


@mcp.tool()
def get_option_quote(symbol: str) -> Dict[str, Any]:
    """
    Get real-time quote for options
    
    Args:
        symbol: Option symbol in format like 'AAPL230317P160000.US'
               Can be obtained from option chain API
        
    Returns:
        Dict containing option quote data including:
        - Basic quote data (price, volume etc.)
        - Option specific data:
          - Implied volatility
          - Open interest
          - Strike price
          - Contract type
          - Underlying symbol
          etc.
    """
    try:
        resp = ctx.option_quote([symbol])

        if not resp:
            return {"error": "No data returned"}

        quote_data = resp[0]
        return {
            # Basic quote data
            "symbol": quote_data.symbol,
            "last_price": quote_data.last_done,
            "prev_close": quote_data.prev_close,
            "open": quote_data.open,
            "high": quote_data.high,
            "low": quote_data.low,
            "timestamp": quote_data.timestamp,
            "volume": quote_data.volume,
            "turnover": quote_data.turnover,
            "trade_status": quote_data.trade_status,

            # Option specific data
            "option_data": {
                "implied_volatility": quote_data.implied_volatility,
                "open_interest": quote_data.open_interest,
                "expiry_date": quote_data.expiry_date,
                "strike_price": quote_data.strike_price,
                "contract_multiplier": quote_data.contract_multiplier,
                "contract_type": quote_data.contract_type,  # 'A' for American, 'U' for European
                "contract_size": quote_data.contract_size,
                "direction": quote_data.direction,  # 'P' for put, 'C' for call
                "historical_volatility": quote_data.historical_volatility,
                "underlying_symbol": quote_data.underlying_symbol
            }
        }

    except Exception as e:
        logging.error(f"Error getting option quote for {symbol}: {str(e)}")
        return {"error": str(e)}


@mcp.tool()
def get_trades(symbol: str, count: int = 100) -> Dict[str, Any]:
    """
    Get trade details/records for a security
    
    Args:
        symbol: Security code in ticker.region format, e.g. 700.HK
        count: Number of trade records to request (max 1000)
        
    Returns:
        Dict containing trade records including:
        - Trade price
        - Trade volume
        - Trade timestamp
        - Trade type
        - Trade direction
        - Trade session
    """
    try:
        if count > 1000:
            return {"error": "Count cannot exceed 1000"}

        resp = ctx.trades(symbol, count)

        if not resp:
            return {"error": "No data returned"}

        trades_list = []
        for trade in resp:
            trades_list.append({
                "price": trade.price,
                "volume": trade.volume,
                "timestamp": trade.timestamp,
                "trade_type": trade.trade_type,
                "direction": trade.direction,
                "trade_session": trade.trade_session
            })

        return {
            "symbol": symbol,
            "trades": trades_list
        }

    except Exception as e:
        logging.error(f"Error getting trades for {symbol}: {str(e)}")
        return {"error": str(e)}


@mcp.tool()
def get_intraday(symbol: str) -> Dict[str, Any]:
    """
    Get intraday data (price and volume by minute) for a security
    
    Args:
        symbol: Security code in ticker.region format, e.g. 700.HK
        
    Returns:
        Dict containing intraday data including:
        - Price
        - Volume
        - Turnover
        - Average price
        By minute intervals
    """
    try:
        resp = ctx.intraday(symbol)

        if not resp:
            return {"error": "No data returned"}

        intraday_list = []
        for line in resp:
            intraday_list.append({
                "price": line.price,
                "timestamp": line.timestamp,
                "volume": line.volume,
                "turnover": line.turnover,
                "avg_price": line.avg_price
            })

        return {
            "symbol": symbol,
            "intraday_lines": intraday_list
        }

    except Exception as e:
        logging.error(f"Error getting intraday data for {symbol}: {str(e)}")
        return {"error": str(e)}


@mcp.tool()
def get_option_chain_dates(symbol: str) -> Dict[str, Any]:
    """
    Get option chain expiry dates list for a security
    
    Args:
        symbol: Security code in ticker.region format, e.g. AAPL.US
        
    Returns:
        Dict containing list of option expiry dates in YYMMDD format
    """
    try:
        resp = ctx.option_chain_expiry_date_list(symbol)

        if not resp:
            return {"error": "No data returned"}

        expiry_dates = []
        for date in resp:
            expiry_dates.append(date.strftime("%Y%m%d"))

        return {
            "symbol": symbol,
            "expiry_dates": expiry_dates
        }

    except Exception as e:
        logging.error(f"Error getting option chain dates for {symbol}: {str(e)}")
        return {"error": str(e)}


@mcp.tool()
def get_option_chain_info(symbol: str, expiry_date: int) -> Dict[str, Any]:
    """
    Get option chain information for a specific expiry date
    
    Args:
        symbol: Security code in ticker.region format, e.g. AAPL.US
        expiry_date: Option expiry date in YYYYMMDD format, e.g. 20250120
        
    Returns:
        Dict containing option chain information including:
        - Strike prices
        - Call option symbols
        - Put option symbols
        For the specified expiry date
    """
    try:
        ## format input expiry_date from YYMMDD to date object
        expiry_date = datetime.strptime(str(expiry_date), "%Y%m%d")
        resp = ctx.option_chain_info_by_date(symbol, expiry_date)

        if not resp:
            return {"error": "No data returned"}

        strikes_list = []
        for strike in resp:
            strikes_list.append({
                "strike_price": strike.price,
                "call_symbol": strike.call_symbol,
                "put_symbol": strike.put_symbol,
                "is_standard": strike.standard
            })

        return {
            "symbol": symbol,
            "expiry_date": expiry_date,
            "strikes": strikes_list
        }

    except Exception as e:
        logging.error(f"Error getting option chain info for {symbol} expiry {expiry_date}: {str(e)}")
        return {"error": str(e)}


@mcp.tool()
def get_candlesticks(symbol: str, period: str, count: int = 100, adjust_type: str = "NO_ADJUST") -> Dict[str, Any]:
    """
    Get candlestick/K-line data for a security
    
    Args:
        symbol: Security code in ticker.region format, e.g. 700.HK
        period: K-line period, valid values: 
               "1m", "5m", "15m", "30m", "60m", "1d", "1w", "1M"
        count: Number of K-lines to request (max 1000)
        adjust_type: Price adjustment type, valid values:
                    "NO_ADJUST" - No adjustment
                    "FORWARD" - Forward adjustment
                    "BACKWARD" - Backward adjustment
        
    Returns:
        Dict containing K-line data including:
        - Open, high, low, close prices
        - Volume
        - Turnover
        - Timestamp
    """
    try:
        # Convert period string to Period enum
        period_map = {
            "1m": Period.Min_1,
            "5m": Period.Min_5,
            "15m": Period.Min_15,
            "30m": Period.Min_30,
            "60m": Period.Min_60,
            "1d": Period.Day,
            "1w": Period.Week,
            "1M": Period.Month
        }

        # Convert adjust_type string to AdjustType enum
        adjust_map = {
            "NO_ADJUST": AdjustType.NoAdjust,
            "FORWARD": AdjustType.ForwardAdjust
        }

        if period not in period_map:
            return {"error": f"Invalid period. Valid values are: {', '.join(period_map.keys())}"}

        if adjust_type not in adjust_map:
            return {"error": f"Invalid adjust_type. Valid values are: {', '.join(adjust_map.keys())}"}

        if count > 1000:
            return {"error": "Count cannot exceed 1000"}

        resp = ctx.candlesticks(
            symbol,
            period_map[period],
            count,
            adjust_map[adjust_type]
        )

        if not resp:
            return {"error": "No data returned"}

        candles_list = []
        for candle in resp:
            candles_list.append({
                "close": candle.close,
                "open": candle.open,
                "low": candle.low,
                "high": candle.high,
                "volume": candle.volume,
                "turnover": candle.turnover,
                "timestamp": candle.timestamp
            })

        return {
            "symbol": symbol,
            "period": period,
            "adjust_type": adjust_type,
            "candles": candles_list
        }

    except Exception as e:
        logging.error(f"Error getting candlesticks for {symbol}: {str(e)}")
        return {"error": str(e)}


@mcp.tool()
def get_calc_indexes(symbol: str, calc_indexes: list[int]) -> Dict[str, Any]:
    """
    Get calculated indexes for a security
    
    Args:
        symbol: Security code in ticker.region format, e.g. AAPL.US
        calc_indexes: List of index types to calculate (required), valid values:
                     [1] - Last done price
                     ...
                     [40] - Rho (options)
        
    Returns:
        Dict containing requested calculated indexes data
    """
    try:
        # Validate calc_indexes
        if not calc_indexes:
            return {"error": "calc_indexes is required"}
            
        if not all(isinstance(x, int) for x in calc_indexes):
            return {"error": "calc_indexes must be a list of integers"}
            
        if not all(1 <= x <= 40 for x in calc_indexes):
            return {"error": "calc_indexes values must be between 1 and 40"}

        # Map integer values to CalcIndex types
        calc_index_map = {
            1: CalcIndex.LastDone,
            2: CalcIndex.ChangeValue,
            3: CalcIndex.ChangeRate,
            4: CalcIndex.Volume,
            5: CalcIndex.Turnover,
            6: CalcIndex.YtdChangeRate,
            7: CalcIndex.TurnoverRate,
            8: CalcIndex.TotalMarketValue,
            9: CalcIndex.CapitalFlow,
            10: CalcIndex.Amplitude,
            11: CalcIndex.VolumeRatio,
            12: CalcIndex.PeTtmRatio,
            13: CalcIndex.PbRatio,
            14: CalcIndex.DividendRatioTtm,
            15: CalcIndex.FiveDayChangeRate,
            16: CalcIndex.TenDayChangeRate,
            17: CalcIndex.HalfYearChangeRate,
            18: CalcIndex.FiveMinutesChangeRate,
            19: CalcIndex.ExpiryDate,
            20: CalcIndex.StrikePrice,
            21: CalcIndex.UpperStrikePrice,
            22: CalcIndex.LowerStrikePrice,
            23: CalcIndex.OutstandingQty,
            24: CalcIndex.OutstandingRatio,
            25: CalcIndex.Premium,
            26: CalcIndex.ItmOtm,
            27: CalcIndex.ImpliedVolatility,
            28: CalcIndex.WarrantDelta,
            29: CalcIndex.CallPrice,
            30: CalcIndex.ToCallPrice,
            31: CalcIndex.EffectiveLeverage,
            32: CalcIndex.LeverageRatio,
            33: CalcIndex.ConversionRatio,
            34: CalcIndex.BalancePoint,
            35: CalcIndex.OpenInterest,
            36: CalcIndex.Delta,
            37: CalcIndex.Gamma,
            38: CalcIndex.Theta,
            39: CalcIndex.Vega,
            40: CalcIndex.Rho
        }

        # Convert integers to CalcIndex types (not instances)
        calc_index_types = [calc_index_map[idx] for idx in calc_indexes]  # Remove the ()
        resp = ctx.calc_indexes([symbol], calc_index_types)

        if not resp:
            return {"error": "No data returned"}

        index_data = resp[0]
        result = {
            "symbol": index_data.symbol,
            "indexes": {}
        }

        # Map index values based on requested calc_indexes
        index_map = {
            1: ("last_done", index_data.last_done),
            2: ("change_val", index_data.change_val),
            3: ("change_rate", index_data.change_rate),
            4: ("volume", index_data.volume),
            5: ("turnover", index_data.turnover),
            6: ("ytd_change_rate", index_data.ytd_change_rate),
            7: ("turnover_rate", index_data.turnover_rate),
            8: ("total_market_value", index_data.total_market_value),
            9: ("capital_flow", index_data.capital_flow),
            10: ("amplitude", index_data.amplitude),
            11: ("volume_ratio", index_data.volume_ratio),
            12: ("pe_ttm_ratio", index_data.pe_ttm_ratio),
            13: ("pb_ratio", index_data.pb_ratio),
            14: ("dividend_ratio_ttm", index_data.dividend_ratio_ttm),
            15: ("five_day_change_rate", index_data.five_day_change_rate),
            16: ("ten_day_change_rate", index_data.ten_day_change_rate),
            17: ("half_year_change_rate", index_data.half_year_change_rate),
            18: ("five_minutes_change_rate", index_data.five_minutes_change_rate)
        }

        # Add option-specific indexes if available
        option_indexes = {
            19: ("expiry_date", getattr(index_data, "expiry_date", None)),
            20: ("strike_price", getattr(index_data, "strike_price", None)),
            25: ("premium", getattr(index_data, "premium", None)),
            26: ("itm_otm", getattr(index_data, "itm_otm", None)),
            27: ("implied_volatility", getattr(index_data, "implied_volatility", None)),
            35: ("open_interest", getattr(index_data, "open_interest", None)),
            36: ("delta", getattr(index_data, "delta", None)),
            37: ("gamma", getattr(index_data, "gamma", None)),
            38: ("theta", getattr(index_data, "theta", None)),
            39: ("vega", getattr(index_data, "vega", None)),
            40: ("rho", getattr(index_data, "rho", None))
        }

        # Add warrant-specific indexes if available
        warrant_indexes = {
            21: ("upper_strike_price", getattr(index_data, "upper_strike_price", None)),
            22: ("lower_strike_price", getattr(index_data, "lower_strike_price", None)),
            23: ("outstanding_qty", getattr(index_data, "outstanding_qty", None)),
            24: ("outstanding_ratio", getattr(index_data, "outstanding_ratio", None)),
            28: ("warrant_delta", getattr(index_data, "warrant_delta", None)),
            29: ("call_price", getattr(index_data, "call_price", None)),
            30: ("to_call_price", getattr(index_data, "to_call_price", None)),
            31: ("effective_leverage", getattr(index_data, "effective_leverage", None)),
            32: ("leverage_ratio", getattr(index_data, "leverage_ratio", None)),
            33: ("conversion_ratio", getattr(index_data, "conversion_ratio", None)),
            34: ("balance_point", getattr(index_data, "balance_point", None))
        }

        # Combine all index maps
        index_map.update(option_indexes)
        index_map.update(warrant_indexes)

        # Add requested indexes to result
        for idx in calc_indexes:
            if idx in index_map:
                key, value = index_map[idx]
                if value is not None:  # Only add non-None values
                    result["indexes"][key] = value

        return result

    except Exception as e:
        logging.error(f"Error getting calc indexes for {symbol}: {str(e)}")
        return {"error": str(e)}


@mcp.tool()
def get_security_list(market: str = "US", category: str = "OVERNIGHT") -> Dict[str, Any]:
    """
    Get security list for a specific market and category
    
    Args:
        market: Market code, currently only supports "US"
        category: Market category, currently only supports "OVERNIGHT"
        
    Returns:
        Dict containing list of securities including:
        - Symbol
        - Name in Chinese
        - Name in Traditional Chinese
        - Name in English
    """
    try:
        # Convert market string to Market enum
        market_map = {
            "US": Market.US,
            "HK": Market.HK,
            "CN": Market.CN,
            "SG": Market.SG
        }
        
        # Convert category string to SecurityListCategory enum
        category_map = {
            "OVERNIGHT": SecurityListCategory.Overnight
        }
        
        if market not in market_map:
            return {"error": f"Invalid market. Valid values are: {', '.join(market_map.keys())}"}
            
        if category not in category_map:
            return {"error": f"Invalid category. Valid values are: {', '.join(category_map.keys())}"}
            
        resp = ctx.security_list(
            market_map[market],
            category_map[category]
        )
        
        if not resp:
            return {"error": "No data returned"}
            
        securities_list = []
        for security in resp:
            securities_list.append({
                "symbol": security.symbol,
                "name_cn": security.name_cn,
                "name_hk": security.name_hk,
                "name_en": security.name_en
            })
            
        return {
            "market": market,
            "category": category,
            "securities": securities_list
        }
        
    except Exception as e:
        logging.error(f"Error getting security list for market {market}, category {category}: {str(e)}")
        return {"error": str(e)}


def initialize():
    import os
    import sys

    # Save the original stdout/stderr
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    # Redirect stdout/stderr to devnull to suppress unwanted output
    devnull = open(os.devnull, 'w')
    sys.stdout = devnull
    sys.stderr = devnull

    # Get configuration from environment variables
    app_key = os.environ.get('LONGPORT_APP_KEY')
    app_secret = os.environ.get('LONGPORT_APP_SECRET')
    access_token = os.environ.get('LONGPORT_ACCESS_TOKEN')
    region = os.environ.get('LONGPORT_REGION', 'cn')  # Default to 'cn' if not set
    enable_overnight = os.environ.get('LONGPORT_ENABLE_OVERNIGHT', 'true').lower() == 'true'  # Default to True if not set

    # Validate required environment variables
    missing_vars = []
    if not app_key:
        missing_vars.append('LONGPORT_APP_KEY')
    if not app_secret:
        missing_vars.append('LONGPORT_APP_SECRET')
    if not access_token:
        missing_vars.append('LONGPORT_ACCESS_TOKEN')

    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    logging.basicConfig(level=logging.INFO)

    # Initialize quote context with provided credentials
    global ctx
    ctx = create_quote_context(
        app_key=app_key,
        app_secret=app_secret,
        access_token=access_token,
        region=region,
        enable_overnight=enable_overnight
    )

    # Restore stdout for MCP communication
    sys.stdout = original_stdout
    sys.stderr = original_stderr

    mcp.run(transport="stdio")

    # Clean up
    devnull.close()
