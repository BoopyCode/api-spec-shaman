#!/usr/bin/env python3
"""API Spec Shaman - Because your API docs are more fiction than documentation"""

import json
import sys
import difflib
from typing import Dict, Any
from urllib import request, parse

class APIShaman:
    """The mystical being that reveals what your API *actually* does"""
    
    def __init__(self, spec_file: str):
        """Initialize with the sacred scrolls (that are probably wrong)"""
        with open(spec_file, 'r') as f:
            self.promised_reality = json.load(f)  # What they SAY it does
        self.actual_reality = {}  # What it ACTUALLY does (spoiler: different)
    
    def test_endpoint(self, url: str, method: str = "GET", data: Dict = None) -> Dict:
        """Ask the API spirits what they really think"""
        req = request.Request(url, method=method)
        if data:
            req.data = json.dumps(data).encode()
            req.add_header('Content-Type', 'application/json')
        
        try:
            with request.urlopen(req) as response:
                return {
                    'status': response.status,
                    'body': json.loads(response.read().decode()),
                    'headers': dict(response.getheaders())
                }
        except Exception as e:
            return {'error': str(e), 'status': 'DEMON_POSSESSED'}
    
    def compare_responses(self, endpoint: str, actual: Dict) -> str:
        """Reveal the gap between promise and reality (it's usually a chasm)"""
        promised = self.promised_reality.get('paths', {}).get(endpoint, {})
        
        report = [f"\n🔮 Divining endpoint: {endpoint}"]
        
        # Check if endpoint even exists in spec (often it doesn't)
        if not promised:
            report.append("  👻 Ghost endpoint! Not in spec but works anyway")
            return '\n'.join(report)
        
        # Compare status codes (they never match)
        promised_status = promised.get('responses', {}).get('200', {})
        actual_status = actual.get('status', 666)
        
        if actual_status != 200:
            report.append(f"  ⚡ Expected 200, got {actual_status} (surprise!)")
        
        # Check response structure (hah!)
        if 'schema' in promised_status:
            report.append("  📜 Schema defined (probably ignored by API)")
        
        # Look for undocumented fields (always present)
        if 'body' in actual:
            actual_keys = set(actual['body'].keys())
            if 'properties' in promised_status.get('schema', {}):
                promised_keys = set(promised_status['schema']['properties'].keys())
                extra = actual_keys - promised_keys
                if extra:
                    report.append(f"  🎁 Bonus fields! Undocumented: {extra}")
        
        return '\n'.join(report)
    
    def perform_ritual(self, base_url: str):
        """Main ceremony to reveal API truths"""
        print("🧙‍♂️ API Shaman begins the ritual...\n")
        
        for endpoint in self.promised_reality.get('paths', {}):
            full_url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
            actual = self.test_endpoint(full_url)
            print(self.compare_responses(endpoint, actual))
        
        print("\n✨ Ritual complete. Your API is... unique.")


def main():
    """Because even shamans need a command line"""
    if len(sys.argv) != 3:
        print("Usage: python api_shaman.py <spec.json> <base_url>")
        print("Example: python api_shaman.py api.json http://localhost:8000")
        sys.exit(1)
    
    shaman = APIShaman(sys.argv[1])
    shaman.perform_ritual(sys.argv[2])

if __name__ == "__main__":
    main()
