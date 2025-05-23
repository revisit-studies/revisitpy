import * as React from "react";
import { createRender, useModelState } from "@anywidget/react";
import "./widget.css";

const SequenceComponent = ({ c, participantSequencesCount, max, sum }: { c: any, participantSequencesCount: { [key: string]: number }, max: number, sum: number }) => {
  return (<div className="sequenceComponent">
    {typeof c === "string" ? <div className="sequenceComponentIndividual" title={`${c} = ${participantSequencesCount[c] / max}`} style={{ opacity: participantSequencesCount[c] / max }} /> :
      (<>{c.components.map((ci: any, idx: number) => <SequenceComponent key={idx} c={ci} participantSequencesCount={participantSequencesCount} max={max} sum={sum} />)}</>)}
  </div>);
}

const getFlattenedSequenceList = (d: any[]): any[] => {
  return d.map((a: any) => typeof a === "string" ? a : getFlattenedSequenceList(a.components).flat());
};


function extractInterruptions(d: any) {
  let interruptions: string[] = [];

  // Recursive function to traverse the JSON object
  function traverse(node: any) {
    // Check if the current node has interruptions
    if (node.interruptions) {
      node.interruptions.forEach((interruption: any) => {
        if (interruption.components) {
          interruptions.push(...interruption.components);
        }
      });
    }

    // Check if the current node has components and process them recursively
    if (Array.isArray(node.components)) {
      node.components.forEach((component: any) => {
        if (typeof component === "object") {
          traverse(component);
        }
      });
    }
  }

  // Start traversal from the root JSON object
  traverse(d);

  return interruptions;
}

const Sequence = ({ d, participantSequences }: { d: any, participantSequences: any[] }) => {
  const [participantSequencesCount, max, sum] = React.useMemo(() => {
    const r: { [key: string]: number } = {};

    if (participantSequences.length) {
      const allStimuli = getFlattenedSequenceList(participantSequences).flat();

      const interruptions = extractInterruptions(d);
      console.log(interruptions);


      allStimuli.forEach((s: string) => {
        if (!r[s]) {
          r[s] = 0;
        }
        r[s]++;
      });

      for (let i = 0; i < interruptions.length; i++) {
        // check if key is in r
        if (interruptions[i] in r) {
          delete r[interruptions[i]];
        }
      }

    }

    const sum = Object.values(r).reduce((acc, v) => acc + v, 0);

    const max = Math.max(...Object.values(r));

    return [r, max, sum];

  }, [participantSequences]);

  return (<div className="sequence">
    {d.components.map((c: any, idx: number) => <SequenceComponent key={idx} c={c} participantSequencesCount={participantSequencesCount} max={max} sum={sum} />)}
  </div>);
};

const render = createRender(() => {
  const [config] = useModelState<any>("config");
  const [iframeReady, setIframeReady] = React.useState(0);
  const [page, setPage] = React.useState("study");
  const [sequences, setSequence] = useModelState<any>("sequence");
  const [participantsDataJSON, setParticipantsDataJSON] = useModelState<any>("participants_data_json");
  const [participantsDataTIDY, setParticipantsDataTIDY] = useModelState<any>("participants_data_tidy");

  const ref = React.useRef<HTMLIFrameElement>(null);

  React.useEffect(() => {
    if (iframeReady) {
      ref.current?.contentWindow?.postMessage(
        {
          type: "revisitWidget/CONFIG",
          payload: JSON.stringify(config),
        },
        "http://localhost:8080"
      );
    }
  }, [config, iframeReady]);

  React.useEffect(() => {
    const messageListener = (event: MessageEvent) => {
      if (event.data.type === "revisitWidget/READY") {
        setIframeReady(i => i + 1);
      } else if (event.data.type === "revisitWidget/PYTHON_EXPORT_JSON") {
        setParticipantsDataJSON(event.data.payload);
      } else if (event.data.type === "revisitWidget/PYTHON_EXPORT_TIDY") {
        setParticipantsDataTIDY(event.data.payload);
      } else if (event.data.type === "revisitWidget/SEQUENCE_ARRAY") {
        setSequence(event.data.payload);
      }
    };

    window.addEventListener("message", messageListener);

    return () => {
      window.removeEventListener("message", messageListener);
    };
  }, [config]);

  return (
    <div className="revisit_notebook_widget">
      <div>
        <button onClick={() => { setPage("study"); }} disabled={page === "study"}>Study</button>
        <button onClick={() => { setPage("analysis"); }} disabled={page === "analysis"}>Analysis</button>
      </div>
      <iframe
        ref={ref}
        src={page === "study" ? "http://localhost:8080/__revisit-widget" : "http://localhost:8080/analysis/stats/__revisit-widget"}
        style={{ width: "100%", height: "800px" }}
      />
    </div>
  );
});

export default { render };
