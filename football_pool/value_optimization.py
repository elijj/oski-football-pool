"""
Value Play Detection and Optimization

This module implements advanced value play detection and optimization algorithms
to maximize earnings potential in the football pool.
"""

import logging
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
import json

logger = logging.getLogger(__name__)


@dataclass
class ValuePlay:
    """Represents a value play with optimization metrics."""
    game: str
    team: str
    confidence: int
    value_score: float
    risk_score: float
    upside_potential: float
    downside_risk: float
    contrarian_edge: float
    public_sentiment: float
    sharp_money_indicator: bool
    optimization_recommendation: str


class ValuePlayOptimizer:
    """Advanced value play detection and optimization system."""

    def __init__(self):
        self.value_threshold = 0.7  # Minimum value score for consideration
        self.risk_threshold = 0.3   # Maximum acceptable risk
        self.contrarian_threshold = 0.6  # Minimum contrarian edge

    def analyze_value_plays(self, picks: List[Dict[str, Any]]) -> List[ValuePlay]:
        """Analyze picks for value play opportunities."""
        value_plays = []

        for pick in picks:
            # Calculate value metrics
            value_score = self._calculate_value_score(pick)
            risk_score = self._calculate_risk_score(pick)
            upside_potential = self._calculate_upside_potential(pick)
            downside_risk = self._calculate_downside_risk(pick)
            contrarian_edge = self._calculate_contrarian_edge(pick)
            public_sentiment = self._calculate_public_sentiment(pick)
            sharp_money = self._detect_sharp_money(pick)

            # Create value play object
            value_play = ValuePlay(
                game=pick.get("game", ""),
                team=pick.get("team", ""),
                confidence=pick.get("confidence", 0),
                value_score=value_score,
                risk_score=risk_score,
                upside_potential=upside_potential,
                downside_risk=downside_risk,
                contrarian_edge=contrarian_edge,
                public_sentiment=public_sentiment,
                sharp_money_indicator=sharp_money,
                optimization_recommendation=self._generate_optimization_recommendation(
                    value_score, risk_score, contrarian_edge, sharp_money
                )
            )

            value_plays.append(value_play)

        return value_plays

    def _calculate_value_score(self, pick: Dict[str, Any]) -> float:
        """Calculate value score based on confidence and contrarian edge."""
        confidence = pick.get("confidence", 0)
        contrarian_edge = pick.get("contrarian_edge", "")

        # Base value from confidence (0-1 scale)
        confidence_value = confidence / 20.0

        # Contrarian bonus
        contrarian_bonus = 0.0
        if "contrarian" in contrarian_edge.lower():
            contrarian_bonus = 0.2
        elif "public" in contrarian_edge.lower() and "split" in contrarian_edge.lower():
            contrarian_bonus = 0.1

        # Value play bonus
        value_play = pick.get("value_play", "")
        value_bonus = 0.0
        if "exploit" in value_play.lower():
            value_bonus = 0.15
        elif "advantage" in value_play.lower():
            value_bonus = 0.1

        return min(1.0, confidence_value + contrarian_bonus + value_bonus)

    def _calculate_risk_score(self, pick: Dict[str, Any]) -> float:
        """Calculate risk score (0-1, lower is better)."""
        risk_assessment = pick.get("risk_assessment", "").lower()
        confidence = pick.get("confidence", 0)

        # Base risk from confidence (inverse relationship)
        confidence_risk = 1.0 - (confidence / 20.0)

        # Risk assessment penalty
        risk_penalty = 0.0
        if "high" in risk_assessment:
            risk_penalty = 0.3
        elif "medium" in risk_assessment:
            risk_penalty = 0.15
        elif "low" in risk_assessment:
            risk_penalty = -0.1  # Bonus for low risk

        return max(0.0, min(1.0, confidence_risk + risk_penalty))

    def _calculate_upside_potential(self, pick: Dict[str, Any]) -> float:
        """Calculate upside potential (0-1 scale)."""
        confidence = pick.get("confidence", 0)
        reasoning = pick.get("reasoning", "").lower()

        # Base upside from confidence
        base_upside = confidence / 20.0

        # Reasoning bonuses
        upside_bonus = 0.0
        if "superior" in reasoning:
            upside_bonus = 0.2
        elif "advantage" in reasoning:
            upside_bonus = 0.15
        elif "talent" in reasoning:
            upside_bonus = 0.1

        return min(1.0, base_upside + upside_bonus)

    def _calculate_downside_risk(self, pick: Dict[str, Any]) -> float:
        """Calculate downside risk (0-1 scale)."""
        risk_assessment = pick.get("risk_assessment", "").lower()
        confidence = pick.get("confidence", 0)

        # Base downside from confidence (inverse)
        base_downside = 1.0 - (confidence / 20.0)

        # Risk assessment penalty
        if "high" in risk_assessment:
            return min(1.0, base_downside + 0.3)
        elif "medium" in risk_assessment:
            return min(1.0, base_downside + 0.15)
        else:
            return max(0.0, base_downside - 0.1)

    def _calculate_contrarian_edge(self, pick: Dict[str, Any]) -> float:
        """Calculate contrarian edge (0-1 scale)."""
        contrarian_edge = pick.get("contrarian_edge", "").lower()

        if "contrarian" in contrarian_edge:
            return 0.8
        elif "public" in contrarian_edge and "split" in contrarian_edge:
            return 0.6
        elif "public" in contrarian_edge:
            return 0.4
        else:
            return 0.2

    def _calculate_public_sentiment(self, pick: Dict[str, Any]) -> float:
        """Calculate public sentiment (0-1 scale)."""
        contrarian_edge = pick.get("contrarian_edge", "").lower()

        if "favor" in contrarian_edge:
            return 0.8
        elif "split" in contrarian_edge:
            return 0.5
        else:
            return 0.3

    def _detect_sharp_money(self, pick: Dict[str, Any]) -> bool:
        """Detect if pick aligns with sharp money."""
        confidence = pick.get("confidence", 0)
        contrarian_edge = pick.get("contrarian_edge", "").lower()

        # High confidence + contrarian indicators = sharp money
        if confidence >= 15 and ("sharp" in contrarian_edge or "contrarian" in contrarian_edge):
            return True

        return False

    def _generate_optimization_recommendation(
        self, value_score: float, risk_score: float,
        contrarian_edge: float, sharp_money: bool
    ) -> str:
        """Generate optimization recommendation."""
        if value_score >= 0.8 and risk_score <= 0.3:
            return "MAXIMIZE - High value, low risk"
        elif value_score >= 0.7 and contrarian_edge >= 0.6:
            return "INCREASE - Strong contrarian play"
        elif sharp_money and value_score >= 0.6:
            return "CONSIDER - Sharp money alignment"
        elif value_score >= 0.6 and risk_score <= 0.5:
            return "MODERATE - Balanced play"
        else:
            return "MINIMIZE - High risk, low value"

    def optimize_confidence_allocation(self, value_plays: List[ValuePlay]) -> List[ValuePlay]:
        """Optimize confidence point allocation based on value analysis."""
        # Sort by value score (descending)
        sorted_plays = sorted(value_plays, key=lambda x: x.value_score, reverse=True)

        # Reallocate confidence points based on value
        optimized_plays = []
        total_confidence = 210  # Sum of 1-20

        for i, play in enumerate(sorted_plays):
            # Calculate optimal confidence based on value score
            base_confidence = 20 - i
            value_multiplier = play.value_score
            risk_penalty = play.risk_score * 0.5

            # Optimized confidence
            optimized_confidence = max(1, min(20, int(base_confidence * value_multiplier * (1 - risk_penalty))))

            # Create optimized play
            optimized_play = ValuePlay(
                game=play.game,
                team=play.team,
                confidence=optimized_confidence,
                value_score=play.value_score,
                risk_score=play.risk_score,
                upside_potential=play.upside_potential,
                downside_risk=play.downside_risk,
                contrarian_edge=play.contrarian_edge,
                public_sentiment=play.public_sentiment,
                sharp_money_indicator=play.sharp_money_indicator,
                optimization_recommendation=play.optimization_recommendation
            )

            optimized_plays.append(optimized_play)

        return optimized_plays

    def generate_value_report(self, value_plays: List[ValuePlay]) -> Dict[str, Any]:
        """Generate comprehensive value analysis report."""
        if not value_plays:
            return {"error": "No value plays to analyze"}

        # Calculate aggregate metrics
        avg_value_score = sum(play.value_score for play in value_plays) / len(value_plays)
        avg_risk_score = sum(play.risk_score for play in value_plays) / len(value_plays)
        avg_contrarian_edge = sum(play.contrarian_edge for play in value_plays) / len(value_plays)

        # Count by recommendation
        recommendations = {}
        for play in value_plays:
            rec = play.optimization_recommendation
            recommendations[rec] = recommendations.get(rec, 0) + 1

        # Identify top value plays
        top_value_plays = sorted(value_plays, key=lambda x: x.value_score, reverse=True)[:5]

        # Identify highest risk plays
        high_risk_plays = [play for play in value_plays if play.risk_score >= 0.7]

        # Identify sharp money plays
        sharp_money_plays = [play for play in value_plays if play.sharp_money_indicator]

        return {
            "summary": {
                "total_plays": len(value_plays),
                "average_value_score": round(avg_value_score, 3),
                "average_risk_score": round(avg_risk_score, 3),
                "average_contrarian_edge": round(avg_contrarian_edge, 3)
            },
            "recommendations": recommendations,
            "top_value_plays": [
                {
                    "game": play.game,
                    "team": play.team,
                    "value_score": play.value_score,
                    "recommendation": play.optimization_recommendation
                }
                for play in top_value_plays
            ],
            "high_risk_plays": [
                {
                    "game": play.game,
                    "team": play.team,
                    "risk_score": play.risk_score,
                    "recommendation": play.optimization_recommendation
                }
                for play in high_risk_plays
            ],
            "sharp_money_plays": [
                {
                    "game": play.game,
                    "team": play.team,
                    "value_score": play.value_score,
                    "contrarian_edge": play.contrarian_edge
                }
                for play in sharp_money_plays
            ]
        }
