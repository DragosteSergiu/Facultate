package model;

import lombok.Builder;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

import java.util.List;
import java.util.concurrent.atomic.AtomicReference;

@Getter
@Builder
@RequiredArgsConstructor
public class HandsidesGrammarPair {
    private final String leftHandside;
    private final List<String> rightHandside;

    @Override
    public String toString() {
        var state = new AtomicReference<>("");
        this.rightHandside.stream().
                reduce((a, b) -> a+ " | " + b)
                .ifPresentOrElse(state::set,
                                 () -> {
                    throw new RuntimeException("Something went wrong during displaying the pairs!!");
                });
        return String.format("%s -> %s", leftHandside, state );
    }
}
