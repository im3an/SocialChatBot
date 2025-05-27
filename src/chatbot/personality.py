class Personality:
    def __init__(self, traits_file):
        self.traits = self.load_traits(traits_file)

    def load_traits(self, traits_file):
        with open(traits_file, 'r') as file:
            return file.read().splitlines()

    def get_traits(self):
        return self.traits

    def add_trait(self, trait):
        if trait not in self.traits:
            self.traits.append(trait)

    def remove_trait(self, trait):
        if trait in self.traits:
            self.traits.remove(trait)