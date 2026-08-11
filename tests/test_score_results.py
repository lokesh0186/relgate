import unittest

from src.score_results import exact_quote_support


def sample_case() -> dict:
    return {
        "change_summary": "Scale queue workers.",
        "diff_or_config": "worker_concurrency: 10",
        "service_context": "Processes notifications.",
        "deployment_plan": "Update config and restart workers.",
        "rollback_plan": "Set concurrency back to 5 if issues arise.",
        "observability_evidence": "Dashboard queue-depth is available.",
        "alerting_evidence": "",
        "owner_oncall_evidence": "Messaging on-call owns the change.",
        "slo_reliability_impact": "No SLO change expected.",
        "blast_radius": "One worker pool.",
        "validation_evidence": "Staging test processed 1,000 messages.",
        "ground_truth": {},
    }


class ExactQuoteSupportTests(unittest.TestCase):
    def test_full_contiguous_quote_is_supported(self):
        self.assertEqual(
            exact_quote_support('Evidence: "Set concurrency back to 5 if issues arise."', sample_case()),
            (1, 0),
        )

    def test_case_and_whitespace_normalization_are_harmless(self):
        self.assertEqual(
            exact_quote_support('Evidence: "set concurrency   BACK to 5 if issues arise."', sample_case()),
            (1, 0),
        )

    def test_prefix_match_alone_is_not_supported(self):
        response = 'Evidence: "Set concurrency back to 5 if issues arise. Fabricated continuation."'
        self.assertEqual(exact_quote_support(response, sample_case()), (1, 1))

    def test_suffix_match_alone_is_not_supported(self):
        response = 'Evidence: "Fabricated preface. Set concurrency back to 5 if issues arise."'
        self.assertEqual(exact_quote_support(response, sample_case()), (1, 1))

    def test_visible_field_label_is_part_of_supplied_bundle(self):
        response = 'Evidence: "Deployment Plan: Update config and restart workers."'
        self.assertEqual(exact_quote_support(response, sample_case()), (1, 0))


if __name__ == "__main__":
    unittest.main()
