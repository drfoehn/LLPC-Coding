import requests
import base64
import json
from django.conf import settings
from django.utils.translation import gettext_lazy as _

def get_loinc_auth_header():
    """Generate the authorization header for LOINC API."""
    credentials = f"{settings.LOINC_API_USERNAME}:{settings.LOINC_API_PASSWORD}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded_credentials}"

def search_loinc(query, language='de', rows=10):
    """
    Search LOINC database for parameters.
    
    Args:
        query (str): Search query
        language (str): Language code ('de' or 'en')
        rows (int): Number of results to return
        
    Returns:
        list: List of matching LOINC entries
    """
    print(f"DEBUG: Starting LOINC search with query: '{query}', language: '{language}', rows: {rows}")
    
    headers = {
        'Authorization': get_loinc_auth_header(),
        'Accept': 'application/json',
    }
    
    # The LOINC API doesn't accept numeric language codes
    # Remove the language parameter if it's not supported
    params = {
        'query': query,
        'rows': rows,
    }
    
    # Only add language parameter if it's explicitly supported by the API
    # if language == 'de':
    #     params['language'] = 'de'
    # elif language == 'en':
    #     params['language'] = 'en'
    
    print(f"DEBUG: API URL: {settings.LOINC_API_BASE_URL}")
    print(f"DEBUG: Headers: {headers}")
    print(f"DEBUG: Params: {params}")
    
    try:
        print("DEBUG: Sending request to LOINC API...")
        response = requests.get(
            settings.LOINC_API_BASE_URL,
            headers=headers,
            params=params,
            timeout=10  # Add timeout to prevent hanging
        )
        
        print(f"DEBUG: Response status code: {response.status_code}")
        print(f"DEBUG: Response headers: {response.headers}")
        
        if response.status_code != 200:
            print(f"DEBUG: Error response content: {response.text}")
            return []
            
        response.raise_for_status()
        
        data = response.json()
        print(f"DEBUG: Response data type: {type(data)}")
        print(f"DEBUG: Response data keys: {data.keys() if isinstance(data, dict) else 'Not a dictionary'}")
        
        # Check if the response has the expected structure
        if isinstance(data, dict):
            # The API returns results in the 'Results' key, not 'loincs'
            if 'Results' in data:
                results = data['Results']
                print(f"DEBUG: Found {len(results)} results in 'Results' key")
                return results
            elif 'loincs' in data:
                results = data['loincs']
                print(f"DEBUG: Found {len(results)} results in 'loincs' key")
                return results
            else:
                print(f"DEBUG: No results found in response. Available keys: {list(data.keys())}")
                return []
        else:
            print(f"DEBUG: Unexpected response format: {json.dumps(data)[:500]}...")
            return []
            
    except requests.exceptions.ConnectionError as e:
        print(f"DEBUG: Connection error: {e}")
        return []
    except requests.exceptions.Timeout as e:
        print(f"DEBUG: Timeout error: {e}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"DEBUG: Request exception: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"DEBUG: JSON decode error: {e}")
        print(f"DEBUG: Response content: {response.text[:500]}...")
        return []
    except Exception as e:
        print(f"DEBUG: Unexpected error: {e}")
        return []

def format_loinc_result(result):
    """Format a LOINC result for display in the UI."""
    return {
        'loinc_code': result.get('LOINC_NUM', ''),
        'name': result.get('LONG_COMMON_NAME', ''),
        'short_name': result.get('SHORTNAME', ''),
        'system': result.get('SYSTEM', ''),
        'class': result.get('CLASS', ''),
        'status': result.get('STATUS', ''),
    } 