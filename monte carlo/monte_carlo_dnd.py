import random
import matplotlib.pyplot as plt

"""Robimy analize monte carlo rzuczania na ability scores w dnd wg. dwóch schematów 
    1. 4d6 bez najniższego wyniku
    2. 7 razy bez najnizszego seta"""


def dnd_4d6_min(n, dice=4, dice_max_val=6):
    """

    :param dice:
    :param dice_max_val:
    :param n: ilość powtórzeń zdarzenia
    :return: lista z prawdopodobieństwem i możliwymi wartosciami

    działanie - rzucamy 4 razy koscią d6 odejmujemy najmniejszy wynik
    """
    output_list = []
    for num in range(3, dice_max_val * (dice - 1) + 1):
        output_list.append([num, 0])  # pozniej bedziemy dodawać do list wyniki
    for i in range(0, n):
        s_omega = [random.randint(1, 6) for result in range(1, 5)]
        minimal_val = min(s_omega)
        sum_omega = sum(s_omega) - minimal_val - 3  # -1 bo indeksujemy od 0 zatem zeby nie wyjsc poza zakres musimy dac ograniczenie
        output_list[sum_omega][1] += 1
    for elements in range(0, dice_max_val * (dice - 1) - 2):
        output_list[elements][1] /= n
    numbers, probablities = zip(*output_list)
    numbers = list(numbers)
    probablities = list(probablities)
    return numbers, probablities


def min_sub_list(a_list):
    min_val = a_list[0]
    for list_ in a_list:
        if sum(list_) < sum(min_val):
            min_val = list_
    return min_val


def dnd_7rolls_without_the_lowest(n, dice=4, dice_max_val=6, turns=7):
    """

    :param turns: ilosc rund po ktorych odejmujemy najmniejsza sume kosci
    :param n: ilość powtórzeń doświadczenia losowego
    :param dice: ilosc kosci
    :param dice_max_val: maksymalny wynik na kosci, minimalny to 1
    :return: listy z mozliwymi wynikami i prawdopodobienstwem

    Działanie - rzucamy 7 razy w taki sam sposób jak w przykladzie poprzednim do tego odejmujemy najmniejszy z tych 7 rzutow,
    sprawdzamy jak zmieni sie prawdopodobienstwo
    """
    # results
    min_score = 3  # minimalny możliwy wynik: 1+1+1+1 = 4, minus 1 = 3
    max_score = 18  # maksymalny możliwy wynik: 6+6+6+6 = 24, minus 6 = 18

    output_list = []
    for num in range(min_score, max_score + 1):
        output_list.append([num, 0])  # pozniej bedziemy dodawać do list wyniki
        # mamy [liczba która może wypaść, ilość wypadnięć]
    print(output_list)

    # ilosc powtórzeń
    for i in range(n):
        # generujemy po 7 powtózeń na turę
        one_turn = []  # każde doświadczenie to bedzie rzut 4d6 7 razy i odrzucenie najmniejszego wyniku
        for turn in range(turns):
            rolls = [random.randint(1, 6) for result in range(dice)]
            total = sum(rolls) - min(rolls)
            one_turn.append(total)

        # usuwamy najmniejszy wynik ze wszystkich tur
        one_turn.remove(min(one_turn))
        for total in one_turn:
            output_list[total - min_score][1] += 1  # w naszym przypadku 4 - 1 bo 3 to najnizszy wynik jaki mozemy uzyskac

    for i in range(len(output_list)):
        output_list[i][1] /= 6 * n

    numbers, probablities = zip(*output_list)
    numbers = list(numbers)
    probablities = list(probablities)
    return numbers, probablities


if __name__ == "__main__":
    numbers_1, probabilities_1 = dnd_4d6_min(100000)
    numbers_2, probabilities_2 = dnd_7rolls_without_the_lowest(1000)
    print(sum(probabilities_2), sum(probabilities_1), "czy jest 1?")

    plt.scatter(numbers_2, probabilities_2, edgecolor="red", alpha=0.9, label="6 rolls")
    plt.scatter(numbers_1, probabilities_1, edgecolor='steelblue', alpha=0.9, label="7 rolls without the lowest")

    plt.title("analiza dwóch rodzajów rzutów", fontsize=16, fontweight='bold', pad=20)
    plt.xlabel("wyniki", fontsize=12)
    plt.ylabel("prawdopodobieństwo", fontsize=12)
    plt.legend()
    # Grid and aesthetics
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.gca().set_facecolor('#f8f9fa')

    plt.savefig("dnd4d6")
    plt.show()
    plt.close()
