from abc import ABC, abstractmethod

# Interface de stratégie
class PromotionStrategy(ABC):
    @abstractmethod
    def apply_discount(self, price, quantity):
        pass

# Stratégie 1 : Pas de réduction
class NoPromotion(PromotionStrategy):
    def apply_discount(self, price, quantity):
        return price * quantity

# Stratégie 2 : Réduction fixe de 10%
class FixedDiscountPromotion(PromotionStrategy):
    def apply_discount(self, price, quantity):
        return price * quantity * 0.90

# Stratégie 3 : Réduction selon la quantité
class QuantityBasedPromotion(PromotionStrategy):
    def apply_discount(self, price, quantity):
        if quantity >= 10:
            return price * quantity * 0.85
        elif quantity >= 5:
            return price * quantity * 0.95
        return price * quantity

# Contexte d'utilisation
class PromotionContext:
    def __init__(self, strategy: PromotionStrategy):
        self.strategy = strategy

    def calculate_total(self, price, quantity):
        return self.strategy.apply_discount(price, quantity)
