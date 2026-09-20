"""Check emitted token-action inputs against an independently sourced interface."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ActionInputsTests(unittest.TestCase):
    def test_token_steps_supply_the_reviewed_actions_required_inputs(self):
        contract = json.loads((ROOT/'tests/fixtures/app-token-input-contract.json').read_text())
        guide = (ROOT/'UNIVERSAL_PROJECT_GOVERNANCE_GUIDE.md').read_text()
        steps = re.findall(r'uses: actions/create-github-app-token@\{\{ACTIONS_CREATE_APP_TOKEN_SHA\}\}\n        with:\n((?:          .+\n)+)', guide)
        self.assertEqual(len(steps), 3)
        for step in steps:
            fields = dict(re.findall(r'^          ([a-z][a-z0-9-]*): (.+)$', step, re.M))
            with self.subTest(step=fields):
                self.assertTrue(set(contract['required_inputs']) <= fields.keys(), 'missing required pinned-action input')
                self.assertNotIn(contract['unsupported_input'], fields)
                self.assertEqual(set(fields), set(contract['required_inputs'] + contract['used_optional_inputs']))
                self.assertEqual(fields['private-key'], '${{ secrets.GOVERNANCE_APP_PRIVATE_KEY }}')
                self.assertEqual(fields['permission-contents'], 'write')
                self.assertEqual(fields['permission-statuses'], 'write')
                self.assertEqual(fields['app-id'], '${{ vars.GOVERNANCE_APP_ID }}')
                self.assertEqual(fields['skip-token-revoke'], 'true')


if __name__ == '__main__':
    unittest.main()
