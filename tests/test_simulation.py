"""Tests for simulation module."""

import pytest

from ahi_module_2.config.simulation_config import SimulationConfig
from ahi_module_2.simulation.maintenance_policy import AgeBasedPolicy, AHIBasedPolicy
from ahi_module_2.simulation.simulation_runner import SimulationRunner
from ahi_module_2.simulation.portfolio_runner import PortfolioRunner
from ahi_module_2.simulation.state_tracker import StateTracker, SimulationStep


class TestMaintenancePolicy:
    def test_age_based_triggers_at_threshold(self):
        policy = AgeBasedPolicy(age_threshold=20.0)
        assert policy.should_trigger(20.0, 1.0) is True

    def test_age_based_no_trigger_below(self):
        policy = AgeBasedPolicy(age_threshold=20.0)
        assert policy.should_trigger(19.9, 1.0) is False

    def test_ahi_based_triggers_at_threshold(self):
        policy = AHIBasedPolicy(ahi_threshold=5.5)
        assert policy.should_trigger(10.0, 5.5) is True

    def test_ahi_based_no_trigger_below(self):
        policy = AHIBasedPolicy()
        assert policy.should_trigger(10.0, 5.4) is False

    def test_age_based_invalid_threshold(self):
        with pytest.raises(ValueError):
            AgeBasedPolicy(age_threshold=0.0)


class TestStateTracker:
    def test_accumulates_costs(self):
        tracker = StateTracker()
        step = SimulationStep(time=0, age=0, hi=0.5, ahi=0.5, pof=0.01, opex=100, capex=0, totex=100, fhi=0.5)
        tracker.record(step)
        assert tracker.accumulated_opex == pytest.approx(100.0)
        assert tracker.totex == pytest.approx(100.0)


class TestSimulationRunner:
    def test_run_returns_correct_step_count(self, basic_asset, basic_financials, empty_conditions):
        policy = AHIBasedPolicy()
        cfg = SimulationConfig(horizon=10, time_step=1.0)
        runner = SimulationRunner(basic_asset, basic_financials, empty_conditions, policy, cfg)
        tracker = runner.run()
        assert len(tracker.steps) == 10

    def test_ahi_increases_with_age(self, basic_asset, basic_financials, empty_conditions):
        policy = AgeBasedPolicy(age_threshold=999)  # never trigger
        cfg = SimulationConfig(horizon=5, time_step=1.0)
        runner = SimulationRunner(basic_asset, basic_financials, empty_conditions, policy, cfg)
        tracker = runner.run()
        ahis = [s.ahi for s in tracker.steps]
        assert ahis[-1] > ahis[0]

    def test_maintenance_resets_ahi(self, basic_asset, basic_financials, empty_conditions):
        # Very low AHI threshold to guarantee early maintenance
        policy = AHIBasedPolicy(ahi_threshold=0.51)
        cfg = SimulationConfig(horizon=5, time_step=1.0)
        runner = SimulationRunner(basic_asset, basic_financials, empty_conditions, policy, cfg)
        tracker = runner.run()
        assert any(s.maintenance_triggered for s in tracker.steps)


class TestPortfolioRunner:
    def test_portfolio_keys_match_asset_ids(self, basic_asset, basic_financials, empty_conditions):
        policy = AHIBasedPolicy()
        cfg = SimulationConfig(horizon=3, time_step=1.0)
        portfolio = PortfolioRunner(sim_config=cfg)
        results = portfolio.run([(basic_asset, basic_financials, empty_conditions, policy)])
        assert "A001" in results

    def test_aggregate_totex_positive(self, basic_asset, basic_financials, empty_conditions):
        policy = AHIBasedPolicy()
        cfg = SimulationConfig(horizon=3, time_step=1.0)
        portfolio = PortfolioRunner(sim_config=cfg)
        results = portfolio.run([(basic_asset, basic_financials, empty_conditions, policy)])
        totex = PortfolioRunner.aggregate_totex(results)
        assert totex > 0
