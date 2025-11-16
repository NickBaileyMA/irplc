"""
Example application demonstrating iRacing OAuth client usage
"""

import argparse
import json
import time
from typing import List, Dict, Any, Union, cast
from iracing_oauth_client import IRacingOAuthClient, Config
from data_api import IRacingDataAPI


def fetch_member_info(data_api: IRacingDataAPI) -> None:
    """Fetch and display member information."""
    print("\n" + "="*50)
    print("FETCHING MEMBER INFORMATION")
    print("="*50)
    
    member_info = data_api.get_member_info(cust_ids=[57575])
    if member_info:
        print(f"✅ Successfully retrieved member information")
        # iRacing member data comes back in a 'members' array
        if 'members' in member_info and member_info['members']:
            member_data = member_info['members'][0]  # First member
            print(f"   Display Name: {member_data.get('display_name', 'N/A')}")
            print(f"   Customer ID: {member_data.get('cust_id', 'N/A')}")
            print(f"   Member Since: {member_data.get('member_since', 'N/A')}")
            print(f"   Last Login: {member_data.get('last_login', 'N/A')}")
            print(f"   Flair: {member_data.get('flair_name', 'N/A')} ({member_data.get('flair_shortname', 'N/A')})")
            print(f"   AI Driver: {member_data.get('ai', False)}")
        else:
            print(f"   Raw response: {json.dumps(member_info, indent=2)}")
    else:
        print("❌ Failed to retrieve member information")


def fetch_series_list(data_api: IRacingDataAPI) -> None:
    """Fetch and display series list."""
    print("\n" + "="*50)
    print("FETCHING SERIES LIST")
    print("="*50)
    
    series_list = data_api.get_series_list()
    if series_list:
        # Handle both direct list response and wrapped response
        series_data: List[Dict[str, Any]]
        if isinstance(series_list, list):
            series_data = series_list
        else:
            # Extract data from dict response, ensure it's a list
            extracted_data = series_list.get('data', series_list)
            series_data = extracted_data if isinstance(extracted_data, list) else []
            
        print(f"✅ Successfully retrieved {len(series_data)} series")
        
        # Show first few series as examples
        for i, series in enumerate(cast(List[Dict[str, Any]], series_data)[:3]):
            print(f"   {i+1}. {series.get('series_name', 'Unknown')} (ID: {series.get('series_id', 'N/A')})")
        
        if len(series_data) > 3:
            print(f"   ... and {len(series_data) - 3} more series")
    else:
        print("❌ Failed to retrieve series list")


def fetch_cars_list(data_api: IRacingDataAPI) -> None:
    """Fetch and display cars list."""
    print("\n" + "="*50)
    print("FETCHING CARS LIST")
    print("="*50)
    
    cars_list = data_api.get_cars_list()
    if cars_list:
        # Handle both direct list response and wrapped response
        cars_data: List[Dict[str, Any]]
        if isinstance(cars_list, list):
            cars_data = cars_list
        else:
            # Extract data from dict response, ensure it's a list
            extracted_data = cars_list.get('data', cars_list)
            cars_data = extracted_data if isinstance(extracted_data, list) else []
            
        print(f"✅ Successfully retrieved {len(cars_data)} cars")
        
        # Show first few cars as examples
        for i, car in enumerate(cast(List[Dict[str, Any]], cars_data)[:3]):
            print(f"   {i+1}. {car.get('car_name', 'Unknown')} (ID: {car.get('car_id', 'N/A')})")
        
        if len(cars_data) > 3:
            print(f"   ... and {len(cars_data) - 3} more cars")
    else:
        print("❌ Failed to retrieve cars list")


def fetch_tracks_list(data_api: IRacingDataAPI) -> None:
    """Fetch and display tracks list."""
    print("\n" + "="*50)
    print("FETCHING TRACKS LIST")
    print("="*50)
    
    tracks_list = data_api.get_tracks_list()
    if tracks_list:
        # Handle both direct list response and wrapped response
        tracks_data: List[Dict[str, Any]]
        if isinstance(tracks_list, list):
            tracks_data = tracks_list
        else:
            # Extract data from dict response, ensure it's a list
            extracted_data = tracks_list.get('data', tracks_list)
            tracks_data = extracted_data if isinstance(extracted_data, list) else []
            
        print(f"✅ Successfully retrieved {len(tracks_data)} tracks")
        
        # Show first few tracks as examples
        for i, track in enumerate(cast(List[Dict[str, Any]], tracks_data)[:3]):
            print(f"   {i+1}. {track.get('track_name', 'Unknown')} (ID: {track.get('track_id', 'N/A')})")
        
        if len(tracks_data) > 3:
            print(f"   ... and {len(tracks_data) - 3} more tracks")
    else:
        print("❌ Failed to retrieve tracks list")


def run_api_calls(data_api: IRacingDataAPI, iteration: int = 0) -> None:
    """
    Execute all API calls.
    
    Args:
        data_api: Authenticated IRacingDataAPI instance
        iteration: Current iteration number (for display purposes)
    """
    if iteration > 0:
        print(f"\n{'='*50}")
        print(f"ITERATION {iteration}")
        print(f"{'='*50}")
    
    try:
        fetch_member_info(data_api)
        fetch_series_list(data_api)
        fetch_cars_list(data_api)
        fetch_tracks_list(data_api)
    except Exception as e:
        print(f"❌ Error during API calls: {e}")


def main():
    """
    Main application demonstrating various iRacing Data API calls.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="iRacing Data API example - fetch data from iRacing's API"
    )
    parser.add_argument(
        "--loop",
        action="store_true",
        help="Loop every 3 minutes for 24 minutes (default: run once and exit)"
    )
    args = parser.parse_args()
    
    # Load configuration
    try:
        config = Config()
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\nPlease ensure you have:")
        print("1. Copied .env.example to .env")
        print("2. Updated .env with your actual iRacing credentials")
        print("3. Registered your client with iRacing for Password Limited Grant")
        return
    
    # Create and authenticate OAuth client
    try:
        oauth_client = IRacingOAuthClient(
            client_id=config.client_id,
            client_secret=config.client_secret,
            username=config.username,
            password=config.password,
            request_timeout=config.request_timeout,
            token_refresh_buffer_seconds=config.token_refresh_buffer_seconds,
            log_level=config.log_level,
            log_format=config.log_format
        )
        
        print("Authenticating with iRacing...")
        if not oauth_client.authenticate(scope=config.scope):
            print("❌ Authentication failed!")
            return
        
        print("✅ Authentication successful!")
        
        # Display authentication status
        print("\n" + "="*50)
        print("AUTHENTICATION STATUS")
        print("="*50)
        print(f"✅ Client is authenticated: {oauth_client.is_authenticated()}")
        print(f"   Access token expires at: {oauth_client.token_expires_at}")
        if oauth_client.refresh_token_expires_at:
            print(f"   Refresh token expires at: {oauth_client.refresh_token_expires_at}")
        print(f"   Granted scope: {oauth_client.scope}")
        
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return
    
    # Create Data API client
    try:
        data_api = IRacingDataAPI(
            oauth_client,
            log_level=config.log_level,
            log_format=config.log_format
        )
    except Exception as e:
        print(f"❌ Failed to create Data API client: {e}")
        return
    
    # Run API calls in a loop
    if args.loop:
        # Loop every 3 minutes for 24 minutes (9 iterations)
        print("\n🔄 Running loop mode (every 3 minutes for 24 minutes)")
        print("   Run without --loop flag to execute a single iteration")
        interval_seconds = 3 * 60  # 3 minutes
        total_duration = 24 * 60  # 24 minutes
        iterations = (total_duration // interval_seconds) + 1  # +1 to include initial run
        
        try:
            for i in range(iterations):
                run_api_calls(data_api, iteration=i+1)
                
                # Sleep until next iteration (except for the last one)
                if i < iterations - 1:
                    print(f"\n⏳ Waiting {interval_seconds // 60} minutes until next iteration...")
                    time.sleep(interval_seconds)
            
            print(f"\n{'='*50}")
            print("ALL ITERATIONS COMPLETE")
            print(f"{'='*50}")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
        except Exception as e:
            print(f"\n❌ Unexpected error during execution: {e}")
    else:
        # Single iteration (default)
        print("\n🔄 Running single iteration")
        print("   Use --loop flag to run every 3 minutes for 24 minutes")
        try:
            run_api_calls(data_api, iteration=1)
            print(f"\n{'='*50}")
            print("SINGLE ITERATION COMPLETE")
            print(f"{'='*50}")
        except Exception as e:
            print(f"\n❌ Unexpected error during execution: {e}")


if __name__ == "__main__":
    main()
